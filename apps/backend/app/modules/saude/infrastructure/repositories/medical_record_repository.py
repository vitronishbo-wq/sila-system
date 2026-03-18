from __future__ import annotations
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from apps.backend.app.modules.saude.infrastructure.models import MedicalRecordModel

class MedicalRecordRepository:

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_appointment_id(self, appointment_id: UUID) -> MedicalRecordModel | None:
        result = await self._session.execute(select(MedicalRecordModel).where(MedicalRecordModel.appointment_id == appointment_id))
        return result.scalar_one_or_none()