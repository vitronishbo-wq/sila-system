"""
Health module repository - Data access layer.
Refatorado para consistência de segurança, timezones e multi-tenancy.
"""

from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from modules.health.models import (
    Appointment,
    HealthRecord,
    HealthService,
    MedicalRecord,
)


class HealthRepository:
    """Repository for Health module database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    # ========================================================================
    # Health Records (Histórico Geral)
    # ========================================================================

    async def create_health_record(
        self,
        user_id: UUID,
        patient_name: Optional[str],
        diagnosis: Optional[str],
        notes: Optional[str],
        region_id: Optional[UUID] = None, # Vinculação regional opcional
    ) -> HealthRecord:
        """Cria um registro de saúde vinculado ao usuário e região."""
        record = HealthRecord(
            user_id=user_id,
            patient_name=patient_name,
            diagnosis=diagnosis,
            notes=notes,
            region_id=region_id
        )
        self.db.add(record)
        await self.db.commit()
        await self.db.refresh(record)
        return record

    async def list_health_records(
        self, 
        user_id: Optional[UUID] = None, 
        region_id: Optional[UUID] = None, # Segurança regional
        skip: int = 0, 
        limit: int = 100
    ) -> List[HealthRecord]:
        """Lista registros com suporte a multi-tenancy regional."""
        stmt = select(HealthRecord).where(HealthRecord.deleted_at.is_(None))

        if user_id:
            stmt = stmt.where(HealthRecord.user_id == user_id)
        if region_id:
            stmt = stmt.where(HealthRecord.region_id == region_id)

        stmt = stmt.offset(skip).limit(limit).order_by(HealthRecord.created_at.desc())
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    # ========================================================================
    # Appointments (Consultas/Agendamentos)
    # ========================================================================

    async def create_appointment(
        self,
        user_id: UUID,
        service_id: UUID,
        scheduled_date: datetime,
        notes: Optional[str] = None,
    ) -> Appointment:
        """Cria um agendamento garantindo que a data seja aware do timezone."""
        # Garante que a data tenha timezone para evitar erros de offset no banco
        if scheduled_date.tzinfo is None:
            scheduled_date = scheduled_date.replace(tzinfo=timezone.utc)

        appointment = Appointment(
            user_id=user_id,
            service_id=service_id,
            scheduled_date=scheduled_date,
            notes=notes,
            status="scheduled",
        )
        self.db.add(appointment)
        await self.db.commit()
        await self.db.refresh(appointment)
        return appointment

    async def cancel_appointment(self, appointment_id: UUID) -> Optional[Appointment]:
        """Cancela uma consulta usando o padrão de delete lógico consistente."""
        appointment = await self.get_appointment(appointment_id)
        if not appointment:
            return None

        appointment.status = "cancelled"
        appointment.deleted_at = datetime.now(timezone.utc) # Corrigido para UTC aware
        
        await self.db.commit()
        await self.db.refresh(appointment)
        return appointment

    # ========================================================================
    # Métodos Utilitários (Getters com Soft-Delete)
    # ========================================================================

    async def get_health_record(self, record_id: UUID) -> Optional[HealthRecord]:
        stmt = select(HealthRecord).where(
            and_(HealthRecord.id == record_id, HealthRecord.deleted_at.is_(None))
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_appointment(self, appointment_id: UUID) -> Optional[Appointment]:
        stmt = (
            select(Appointment)
            .options(
                selectinload(Appointment.service),
                selectinload(Appointment.medical_record),
            )
            .where(and_(Appointment.id == appointment_id, Appointment.deleted_at.is_(None)))
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def delete_health_record(self, record_id: UUID) -> bool:
        """Soft delete seguro."""
        record = await self.get_health_record(record_id)
        if not record:
            return False
        record.deleted_at = datetime.now(timezone.utc)
        await self.db.commit()
        return True

    # Os demais métodos seguem o padrão original, mas utilizando os helpers acima