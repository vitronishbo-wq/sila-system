from __future__ import annotations
import asyncio
import inspect
import os
import time
from importlib import import_module
from typing import Awaitable, Callable
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from apps.backend.app.core.db import AsyncSessionLocal
from apps.backend.app.core.db import engine as write_engine
from apps.backend.app.modules.infrastructure.application.events.registry import EVENT_HANDLERS
from apps.backend.app.modules.infrastructure.application.sagas.execucao_obra_saga import ExecucaoObraSaga
from apps.backend.app.modules.infrastructure.infrastructure.observability.tracing import instrument_sqlalchemy, setup_tracing, start_span
from apps.backend.app.modules.infrastructure.infrastructure.persistence.saga_repository import SQLAlchemySagaRepository
from apps.backend.app.modules.infrastructure.infrastructure.persistence.outbox_repository import SQLAlchemyOutboxRepository
from apps.backend.app.modules.infrastructure.infrastructure.read_model.dashboard_projection_repository import DashboardProjectionRepository
from apps.backend.app.modules.infrastructure.infrastructure.streaming.bi_producer import BIProducer
from apps.backend.app.modules.infrastructure.infrastructure.multi_region.global_id import current_region_code
try:
    from prometheus_client import Counter, Gauge, Histogram
except Exception:
    Counter = Gauge = Histogram = None
PROJECTION_CONSUMER = 'obras_publicas.dashboard_projection'
BI_STREAM_CONSUMER = 'obras_publicas.bi_stream'
EVENTS_PROCESSED_TOTAL = Counter('op_events_processed_total', 'Total de eventos processados no worker de obras publicas', labelnames=('event_type',)) if Counter else None
EVENTS_FAILED_TOTAL = Counter('op_events_failed_total', 'Total de falhas de processamento de eventos no worker de obras publicas', labelnames=('event_type',)) if Counter else None
PENDING_QUEUE_GAUGE = Gauge('op_outbox_pending_batch_size', 'Tamanho do lote pendente capturado por poll') if Gauge else None
BATCH_DURATION_SECONDS = Histogram('op_outbox_batch_duration_seconds', 'Duracao do processamento de lote do outbox de obras publicas') if Histogram else None

def import_string(path: str) -> Callable[..., Awaitable[None]]:
    module_path, func_name = path.rsplit('.', 1)
    module = import_module(module_path)
    return getattr(module, func_name)

class OutboxWorker:

    def __init__(self, *, session_factory: async_sessionmaker[AsyncSession] | None=None, batch_size: int=50, max_failed_attempts: int=15) -> None:
        self._session_factory = session_factory or AsyncSessionLocal
        self._outbox_repo = SQLAlchemyOutboxRepository(session_factory=self._session_factory)
        self._saga_repo = SQLAlchemySagaRepository(session_factory=self._session_factory)
        self._saga = ExecucaoObraSaga(self._saga_repo)
        self._dashboard_projection_repo = DashboardProjectionRepository()
        self._bi_producer = BIProducer()
        self._bi_topic = os.environ.get('OP_BI_TOPIC', 'obras_publicas_events')
        self._region_code = current_region_code()
        self._batch_size = batch_size
        self._max_failed_attempts = max_failed_attempts
        setup_tracing()
        instrument_sqlalchemy(write_engine)

    async def process_batch(self) -> int:
        started_at = time.perf_counter()
        processed = 0
        async with self._session_factory() as session:
            async with session.begin():
                events = await self._outbox_repo.get_pending_for_update(session, limit=self._batch_size, max_failed_attempts=self._max_failed_attempts)
                if PENDING_QUEUE_GAUGE is not None:
                    PENDING_QUEUE_GAUGE.set(len(events))
                for event_row in events:
                    correlation_id = str(event_row.correlation_id or event_row.id)
                    payload = dict(event_row.payload or {})
                    with start_span('obras_publicas.outbox.process_event', {'event_type': event_row.event_type, 'correlation_id': correlation_id, 'tenant_id': event_row.tenant_id}):
                        try:
                            await self._saga.advance(session, event_type=event_row.event_type, payload=payload, correlation_id=correlation_id, tenant_id=event_row.tenant_id)
                            await self._dispatch_event(event_row, session)
                            await self._run_consumer_step(session=session, event_row=event_row, consumer_name=PROJECTION_CONSUMER, operation=lambda: self._dashboard_projection_repo.project(session, event_type=event_row.event_type, payload=payload, tenant_id=event_row.tenant_id, event_id=event_row.id))
                            await self._run_consumer_step(session=session, event_row=event_row, consumer_name=BI_STREAM_CONSUMER, operation=lambda: self._publish_bi_event(event_row))
                            await self._outbox_repo.mark_processed(session, event_row.id)
                            processed += 1
                            if EVENTS_PROCESSED_TOTAL is not None:
                                EVENTS_PROCESSED_TOTAL.labels(event_type=event_row.event_type).inc()
                        except Exception as exc:
                            await self._saga.mark_failed(session, correlation_id=correlation_id, tenant_id=event_row.tenant_id, reason=str(exc))
                            await self._outbox_repo.increment_failed_attempts(session, event_row.id)
                            if EVENTS_FAILED_TOTAL is not None:
                                EVENTS_FAILED_TOTAL.labels(event_type=event_row.event_type).inc()
        if BATCH_DURATION_SECONDS is not None:
            BATCH_DURATION_SECONDS.observe(time.perf_counter() - started_at)
        return processed

    async def run_forever(self, *, interval_seconds: float=2.0) -> None:
        while True:
            try:
                await self.process_batch()
            except Exception:
                await asyncio.sleep(max(interval_seconds, 1.0))
                continue
            await asyncio.sleep(interval_seconds)

    async def _dispatch_event(self, event_row, session: AsyncSession) -> None:
        handlers = EVENT_HANDLERS.get(event_row.event_type, [])
        for handler_path in handlers:
            consumer_name = handler_path
            consumed = await self._outbox_repo.was_consumed(session, event_row.id, consumer_name)
            if consumed:
                continue
            handler = import_string(handler_path)
            kwargs = {'payload': dict(event_row.payload or {}), 'tenant_id': event_row.tenant_id, 'correlation_id': str(event_row.correlation_id or event_row.id)}
            signature = inspect.signature(handler)
            if 'session' in signature.parameters:
                kwargs['session'] = session
            if 'event_type' in signature.parameters:
                kwargs['event_type'] = event_row.event_type
            await handler(**kwargs)
            await self._outbox_repo.register_consumption(session, event_row.id, consumer_name)

    async def _publish_bi_event(self, event_row) -> None:
        payload = dict(event_row.payload or {})
        payload['_meta'] = {'event_type': event_row.event_type, 'tenant_id': event_row.tenant_id, 'correlation_id': str(event_row.correlation_id or event_row.id), 'idempotency_key': event_row.idempotency_key, 'region_code': self._region_code, 'created_at': event_row.created_at.isoformat() if event_row.created_at else None}
        await self._bi_producer.publish(topic=self._bi_topic, payload=payload)

    async def _run_consumer_step(self, *, session: AsyncSession, event_row, consumer_name: str, operation: Callable[[], Awaitable[None]]) -> None:
        consumed = await self._outbox_repo.was_consumed(session, event_row.id, consumer_name)
        if consumed:
            return
        await operation()
        await self._outbox_repo.register_consumption(session, event_row.id, consumer_name)