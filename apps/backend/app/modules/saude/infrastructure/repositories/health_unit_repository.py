from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.modules.saude.infrastructure.models import HealthUnitModel


class HealthUnitRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, health_unit_id: UUID) -> HealthUnitModel | None:
        result = await self._session.execute(
            select(HealthUnitModel).where(HealthUnitModel.id == health_unit_id)
        )
        return result.scalar_one_or_none()
