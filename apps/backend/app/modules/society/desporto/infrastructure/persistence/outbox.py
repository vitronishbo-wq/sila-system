from __future__ import annotations
import asyncio
import os
import socket
from datetime import datetime, timedelta, timezone
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from app.core.db import AsyncSessionLocal
from apps.backend.app.modules.society.desporto.application.events import deserialize_event, serialize_event
from apps.backend.app.modules.society.desporto.application.ports.outbox_repository_port import OutboxMessage, OutboxRepositoryPort
from apps.backend.app.modules.society.desporto.infrastructure.models.outbox_event_model import OutboxEventModel

def _default_worker_id() -> str:
    return f'{socket.gethostname()}-{os.getpid()}'

class InMemoryOutboxRepository(OutboxRepositoryPort):

    def __init__(self) -> None:
        self._events: list[OutboxMessage] = []
        self._lock = asyncio.Lock()

    async def append(self, event: object) -> None:
        event_name, payload = serialize_event(event)
        async with self._lock:
            self._events.append(OutboxMessage(id=None, event=event, event_name=event_name, payload=payload))

    async def pop_batch(self, batch_size: int=100, *, worker_id: str | None=None, lock_ttl_seconds: int=60) -> list[OutboxMessage]:
        if batch_size <= 0:
            return []
        async with self._lock:
            batch = self._events[:batch_size]
            self._events = self._events[batch_size:]
            return batch

    async def mark_processed(self, message: OutboxMessage) -> None:
        return None

    async def mark_failed(self, message: OutboxMessage, *, error: str | None=None, retry_delay_seconds: int=5) -> None:
        if message.id is None:
            async with self._lock:
                self._events.append(message)

class SQLAlchemyOutboxRepository(OutboxRepositoryPort):

    def __init__(self, session_factory: async_sessionmaker[AsyncSession] | None=None) -> None:
        self._session_factory = session_factory or AsyncSessionLocal

    async def append(self, event: object) -> None:
        event_name, payload = serialize_event(event)
        idempotency_key = str(payload.get('event_id') or f'{event_name}-{datetime.now(timezone.utc).isoformat()}')
        model = OutboxEventModel(event_name=event_name, payload=payload, event_version=int(payload.get('version', 1)), schema_version=1, idempotency_key=idempotency_key, processed=False, retries=0, available_at=datetime.now(timezone.utc), locked_by=None, locked_at=None)
        async with self._session_factory() as session:
            session.add(model)
            await session.commit()

    async def pop_batch(self, batch_size: int=100, *, worker_id: str | None=None, lock_ttl_seconds: int=60) -> list[OutboxMessage]:
        if batch_size <= 0:
            return []
        worker = worker_id or _default_worker_id()
        now = datetime.now(timezone.utc)
        stale_before = now - timedelta(seconds=max(lock_ttl_seconds, 1))
        async with self._session_factory() as session:
            async with session.begin():
                stmt = select(OutboxEventModel).where(OutboxEventModel.processed.is_(False), OutboxEventModel.available_at <= now, or_(OutboxEventModel.locked_at.is_(None), OutboxEventModel.locked_at < stale_before)).order_by(OutboxEventModel.created_at.asc()).limit(batch_size).with_for_update(skip_locked=True)
                rows = (await session.execute(stmt)).scalars().all()
                for row in rows:
                    row.locked_by = worker
                    row.locked_at = now
            return [OutboxMessage(id=row.id, event=deserialize_event(row.event_name, dict(row.payload or {})), event_name=row.event_name, payload=dict(row.payload or {}), retries=int(row.retries or 0), locked_by=row.locked_by, locked_at=row.locked_at) for row in rows]

    async def mark_processed(self, message: OutboxMessage) -> None:
        if message.id is None:
            return
        async with self._session_factory() as session:
            row = await session.get(OutboxEventModel, message.id)
            if row is None:
                return
            row.processed = True
            row.processed_at = datetime.now(timezone.utc)
            row.locked_by = None
            row.locked_at = None
            row.last_error = None
            await session.commit()

    async def mark_failed(self, message: OutboxMessage, *, error: str | None=None, retry_delay_seconds: int=5) -> None:
        if message.id is None:
            return
        async with self._session_factory() as session:
            row = await session.get(OutboxEventModel, message.id)
            if row is None:
                return
            row.retries = int(row.retries or 0) + 1
            row.last_error = error
            row.locked_by = None
            row.locked_at = None
            row.available_at = datetime.now(timezone.utc) + timedelta(seconds=max(retry_delay_seconds, 1))
            await session.commit()