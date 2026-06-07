from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.governance.statistics.infrastructure.models.outbox_event_model import (
    OutboxEventModel,
)


class SQLAlchemyOutboxRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def enqueue(
        self, *, event_name: str, aggregate_type: str, aggregate_id: str, payload: dict
    ) -> OutboxEventModel:
        model = OutboxEventModel(
            event_name=event_name,
            aggregate_type=aggregate_type,
            aggregate_id=aggregate_id,
            payload=payload,
            status="pending",
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def list_pending(self, limit: int = 100) -> list[OutboxEventModel]:
        stmt = (
            select(OutboxEventModel)
            .where(OutboxEventModel.status == "pending")
            .order_by(OutboxEventModel.id.asc())
            .limit(limit)
        )
        return list((await self.session.execute(stmt)).scalars().all())
