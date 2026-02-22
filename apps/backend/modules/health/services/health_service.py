from typing import List, Optional, Any
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from modules.health.models.health_record import HealthRecord
from modules.health.schemas.api_schemas import (
    HealthRecordCreate,
    HealthRecordResponse,
    HealthRecordUpdate,
    HealthRecordsListResponse,
    AppointmentResponse,
    CancelAppointmentResponse,
    MedicalRecordResponse
)

class HealthService:
    """Service for managing health records and medical operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_health_record(self, user_id: UUID, payload: HealthRecordCreate) -> HealthRecordResponse:
        db_record = HealthRecord(
            **payload.model_dump(),
            user_id=user_id
        )
        self.db.add(db_record)
        await self.db.commit()
        await self.db.refresh(db_record)
        return HealthRecordResponse.model_validate(db_record)

    async def get_health_record(self, record_id: UUID) -> Optional[HealthRecordResponse]:
        result = await self.db.execute(
            select(HealthRecord).where(HealthRecord.id == record_id)
        )
        record = result.scalar_one_or_none()
        return HealthRecordResponse.model_validate(record) if record else None

    async def list_health_records(self, skip: int = 0, limit: int = 100) -> HealthRecordsListResponse:
        result = await self.db.execute(
            select(HealthRecord).offset(skip).limit(limit)
        )
        records = result.scalars().all()
        items = [HealthRecordResponse.model_validate(r) for r in records]
        return HealthRecordsListResponse(items=items, total=len(items))

    async def update_health_record(self, record_id: UUID, payload: HealthRecordUpdate) -> Optional[HealthRecordResponse]:
        result = await self.db.execute(
            select(HealthRecord).where(HealthRecord.id == record_id)
        )
        record = result.scalar_one_or_none()
        if not record:
            return None

        update_data = payload.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(record, field, value)

        await self.db.commit()
        await self.db.refresh(record)
        return HealthRecordResponse.model_validate(record)

    async def delete_health_record(self, record_id: UUID) -> bool:
        result = await self.db.execute(
            select(HealthRecord).where(HealthRecord.id == record_id)
        )
        record = result.scalar_one_or_none()
        if not record:
            return False

        await self.db.delete(record)
        await self.db.commit()
        return True

    async def list_health_services(self, category: Optional[str] = None, status_filter: Optional[str] = None) -> Any:
        # Lógica para retornar serviços médicos disponíveis
        return {"services": []}

    async def create_appointment(self, user_id: UUID, payload: Any) -> AppointmentResponse:
        # Lógica para criação de agendamento no banco
        return AppointmentResponse(id=str(user_id), status="scheduled")

    async def list_user_appointments(self, user_id: UUID, status_filter: Optional[str] = None) -> Any:
        return {"appointments": []}

    async def cancel_appointment(self, user_id: UUID, appointment_id: str) -> Optional[CancelAppointmentResponse]:
        return CancelAppointmentResponse(id=appointment_id, status="cancelled")

    async def get_medical_record(self, user_id: UUID, appointment_id: str) -> Optional[MedicalRecordResponse]:
        return None