from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.events.registry import (
    TelecomEventRegistry,
    serialize_event,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.ports.outbox_repository_port import (
    OutboxRepositoryPort,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.infrastructure.persistence.outbox_model import (
    OutboxEventModel,
)


@dataclass
class OutboxMessage:
    id: UUID
    event_name: str
    topic: str
    payload: dict
    headers: dict
    processed: bool
    retries: int
    created_at: datetime
    processed_at: datetime | None = None
    last_error: str | None = None


class SQLAlchemyOutboxRepository(OutboxRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def enqueue(self, event: Any) -> OutboxMessage:
        event_name, payload = serialize_event(event)
        topic = TelecomEventRegistry.PUBLISHABLE_EVENTS.get(event_name, event_name)
        row = OutboxEventModel(
            id=uuid4(),
            event_name=event_name,
            topic=topic,
            payload=payload,
            headers={},
            processed=False,
            retries=0,
            created_at=datetime.now(UTC),
        )
        self.session.add(row)
        await self.session.commit()
        await self.session.refresh(row)
        return self._to_message(row)

    async def get_pending(self, *, limit: int = 100) -> list[OutboxMessage]:
        result = await self.session.execute(
            select(OutboxEventModel)
            .where(OutboxEventModel.processed.is_(False))
            .order_by(OutboxEventModel.created_at.asc())
            .limit(limit)
        )
        rows = result.scalars().all()
        return [self._to_message(row) for row in rows]

    async def mark_done(self, message_id: UUID) -> None:
        result = await self.session.execute(
            select(OutboxEventModel).where(OutboxEventModel.id == message_id)
        )
        row = result.scalars().first()
        if row is None:
            return
        row.processed = True
        row.processed_at = datetime.now(UTC)
        row.last_error = None
        await self.session.commit()

    async def increment_retries(self, message_id: UUID, *, error: str | None = None) -> None:
        result = await self.session.execute(
            select(OutboxEventModel).where(OutboxEventModel.id == message_id)
        )
        row = result.scalars().first()
        if row is None:
            return
        row.retries = int(row.retries or 0) + 1
        row.last_error = error
        await self.session.commit()

    @staticmethod
    def _to_message(row: OutboxEventModel) -> OutboxMessage:
        return OutboxMessage(
            id=row.id,
            event_name=row.event_name,
            topic=row.topic,
            payload=dict(row.payload or {}),
            headers=dict(row.headers or {}),
            processed=bool(row.processed),
            retries=int(row.retries or 0),
            created_at=row.created_at,
            processed_at=row.processed_at,
            last_error=row.last_error,
        )
