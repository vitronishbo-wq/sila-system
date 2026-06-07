from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.saude.infrastructure.models import AppointmentModel


class AppointmentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, appointment_id: UUID) -> AppointmentModel | None:
        result = await self._session.execute(
            select(AppointmentModel).where(AppointmentModel.id == appointment_id)
        )
        return result.scalar_one_or_none()
