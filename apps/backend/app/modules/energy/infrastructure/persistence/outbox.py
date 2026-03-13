from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from app.core.db import AsyncSessionLocal
from app.modules.energy.application.events.registry import EnergiaEventRegistry, serialize_event
from app.modules.energy.application.ports.outbox_repository_port import OutboxRepositoryPort
from app.modules.energy.infrastructure.models.outbox_event_model import EnergiaOutboxEventModel

@dataclass
class OutboxMessage:
    id: UUID
    event_name: str
    topic: str
    payload: dict
    headers: dict
    event_version: int
    schema_version: int
    processed: bool
    retries: int
    created_at: datetime
    processed_at: datetime | None = None
    last_error: str | None = None

class SQLAlchemyOutboxRepository(OutboxRepositoryPort):

    def __init__(self, session_factory: async_sessionmaker[AsyncSession] | None=None) -> None:
        self._session_factory = session_factory or AsyncSessionLocal

    async def enqueue(self, event: Any) -> OutboxMessage:
        event_name, payload = serialize_event(event)
        topic = EnergiaEventRegistry.PUBLISHABLE_EVENTS.get(event_name, event_name)
        model = EnergiaOutboxEventModel(id=uuid4(), event_name=event_name, event_version=int(payload.get('version', 1)), schema_version=1, topic=topic, payload=payload, headers={}, processed=False, retries=0, created_at=datetime.now(timezone.utc))
        async with self._session_factory() as session:
            session.add(model)
            await session.commit()
        return self._to_message(model)

    async def get_pending(self, *, limit: int=100) -> list[OutboxMessage]:
        async with self._session_factory() as session:
            result = await session.execute(select(EnergiaOutboxEventModel).where(EnergiaOutboxEventModel.processed.is_(False)).order_by(EnergiaOutboxEventModel.created_at.asc()).limit(limit))
            rows = result.scalars().all()
            return [self._to_message(row) for row in rows]

    async def mark_done(self, message_id: UUID) -> None:
        async with self._session_factory() as session:
            result = await session.execute(select(EnergiaOutboxEventModel).where(EnergiaOutboxEventModel.id == message_id))
            row = result.scalars().first()
            if row is None:
                return
            row.processed = True
            row.processed_at = datetime.now(timezone.utc)
            row.last_error = None
            await session.commit()

    async def increment_retries(self, message_id: UUID, *, error: str | None=None) -> None:
        async with self._session_factory() as session:
            result = await session.execute(select(EnergiaOutboxEventModel).where(EnergiaOutboxEventModel.id == message_id))
            row = result.scalars().first()
            if row is None:
                return
            row.retries = int(row.retries or 0) + 1
            row.last_error = error
            await session.commit()

    @staticmethod
    def _to_message(row: EnergiaOutboxEventModel) -> OutboxMessage:
        return OutboxMessage(id=row.id, event_name=row.event_name, topic=row.topic, payload=dict(row.payload or {}), headers=dict(row.headers or {}), event_version=int(row.event_version or 1), schema_version=int(row.schema_version or 1), processed=bool(row.processed), retries=int(row.retries or 0), created_at=row.created_at, processed_at=row.processed_at, last_error=row.last_error)
