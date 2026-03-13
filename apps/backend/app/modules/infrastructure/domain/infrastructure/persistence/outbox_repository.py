from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from apps.backend.app.core.db import AsyncSessionLocal
from apps.backend.app.modules.infrastructure.application.ports.outbox_repository_port import OutboxRepositoryPort
from apps.backend.app.modules.infrastructure.infrastructure.persistence.outbox_model import OutboxEventConsumptionModel, OutboxEventModel
from apps.backend.app.modules.infrastructure.infrastructure.governance.event_governance import EventGovernanceService

@dataclass
class OutboxMessage:
    id: UUID
    tenant_id: str
    aggregate_type: str
    aggregate_id: str
    event_type: str
    payload: dict
    idempotency_key: str
    correlation_id: str
    created_at: datetime
    processed_at: datetime | None
    failed_attempts: int

class SQLAlchemyOutboxRepository(OutboxRepositoryPort):

    def __init__(self, *, session: AsyncSession | None=None, session_factory: async_sessionmaker[AsyncSession] | None=None) -> None:
        self._session = session
        self._session_factory = session_factory or AsyncSessionLocal
        self._governance = EventGovernanceService()

    async def save(self, *, tenant_id: str, aggregate_type: str, aggregate_id: str, event: Any, correlation_id: str) -> UUID:
        if not hasattr(event, 'event_name') or not hasattr(event, 'to_payload'):
            raise ValueError('Evento invalido para outbox')
        payload = dict(event.to_payload() or {})
        event_id = str(payload.get('event_id') or '')
        if not event_id:
            raise ValueError('Evento sem event_id para idempotencia')
        model = OutboxEventModel(tenant_id=tenant_id, aggregate_type=aggregate_type, aggregate_id=aggregate_id, event_type=str(event.event_name), payload=payload, idempotency_key=event_id, correlation_id=correlation_id, processed_at=None, failed_attempts=0)
        if self._session is not None:
            await self._governance.validate_event(session=self._session, event_name=str(event.event_name), payload=payload)
            self._session.add(model)
            await self._session.flush()
            return model.id
        async with self._session_factory() as session:
            await self._governance.validate_event(session=session, event_name=str(event.event_name), payload=payload)
            session.add(model)
            await session.commit()
            return model.id

    async def get_pending_for_update(self, session: AsyncSession, *, limit: int=50, max_failed_attempts: int=15) -> list[OutboxEventModel]:
        stmt = select(OutboxEventModel).where(OutboxEventModel.processed_at.is_(None), OutboxEventModel.failed_attempts < max_failed_attempts).order_by(OutboxEventModel.created_at.asc()).limit(limit).with_for_update(skip_locked=True)
        result = await session.execute(stmt)
        return list(result.scalars().all())

    async def mark_processed(self, session: AsyncSession, event_id: UUID) -> None:
        row = await session.get(OutboxEventModel, event_id)
        if row is None:
            return
        row.processed_at = datetime.now(timezone.utc)

    async def increment_failed_attempts(self, session: AsyncSession, event_id: UUID) -> None:
        row = await session.get(OutboxEventModel, event_id)
        if row is None:
            return
        row.failed_attempts = int(row.failed_attempts or 0) + 1

    async def was_consumed(self, session: AsyncSession, event_id: UUID, consumer_name: str) -> bool:
        stmt = select(OutboxEventConsumptionModel).where(OutboxEventConsumptionModel.event_id == event_id, OutboxEventConsumptionModel.consumer_name == consumer_name)
        result = await session.execute(stmt)
        return result.scalars().first() is not None

    async def register_consumption(self, session: AsyncSession, event_id: UUID, consumer_name: str) -> None:
        stmt = insert(OutboxEventConsumptionModel).values(event_id=event_id, consumer_name=consumer_name)
        stmt = stmt.on_conflict_do_nothing(index_elements=['event_id', 'consumer_name'])
        await session.execute(stmt)
