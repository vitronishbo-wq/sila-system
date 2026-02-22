"""
Health module repository - Data access layer.

This repository handles all database operations for the Health module
using SQLAlchemy 2.x async patterns.
"""

from datetime import datetime
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
    # Health Records
    # ========================================================================

    async def create_health_record(
        self,
        user_id: UUID,
        patient_name: Optional[str],
        diagnosis: Optional[str],
        notes: Optional[str],
    ) -> HealthRecord:
        """Create a new health record."""
        record = HealthRecord(
            user_id=user_id,
            patient_name=patient_name,
            diagnosis=diagnosis,
            notes=notes,
        )
        self.db.add(record)
        await self.db.commit()
        await self.db.refresh(record)
        return record

    async def get_health_record(self, record_id: UUID) -> Optional[HealthRecord]:
        """Get a health record by ID (excluding soft-deleted)."""
        stmt = select(HealthRecord).where(
            and_(
                HealthRecord.id == record_id,
                HealthRecord.deleted_at.is_(None),
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_health_records(
        self, user_id: Optional[UUID] = None, skip: int = 0, limit: int = 100
    ) -> List[HealthRecord]:
        """List health records (excluding soft-deleted)."""
        stmt = select(HealthRecord).where(HealthRecord.deleted_at.is_(None))

        if user_id:
            stmt = stmt.where(HealthRecord.user_id == user_id)

        stmt = stmt.offset(skip).limit(limit).order_by(HealthRecord.created_at.desc())

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def count_health_records(self, user_id: Optional[UUID] = None) -> int:
        """Count health records (excluding soft-deleted)."""
        stmt = select(func.count(HealthRecord.id)).where(
            HealthRecord.deleted_at.is_(None)
        )

        if user_id:
            stmt = stmt.where(HealthRecord.user_id == user_id)

        result = await self.db.execute(stmt)
        return result.scalar_one() or 0

    async def update_health_record(
        self,
        record_id: UUID,
        patient_name: Optional[str] = None,
        diagnosis: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> Optional[HealthRecord]:
        """Update a health record."""
        record = await self.get_health_record(record_id)
        if not record:
            return None

        if patient_name is not None:
            record.patient_name = patient_name
        if diagnosis is not None:
            record.diagnosis = diagnosis
        if notes is not None:
            record.notes = notes

        await self.db.commit()
        await self.db.refresh(record)
        return record

    async def delete_health_record(self, record_id: UUID) -> bool:
        """Soft delete a health record."""
        record = await self.get_health_record(record_id)
        if not record:
            return False

        record.deleted_at = datetime.utcnow()
        await self.db.commit()
        return True

    # ========================================================================
    # Health Services
    # ========================================================================

    async def list_health_services(
        self, category: Optional[str] = None, status_filter: Optional[str] = None
    ) -> List[HealthService]:
        """List health services with optional filters."""
        stmt = select(HealthService).where(HealthService.deleted_at.is_(None))

        if category:
            stmt = stmt.where(HealthService.category == category)
        if status_filter:
            stmt = stmt.where(HealthService.status == status_filter)

        stmt = stmt.order_by(HealthService.name)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def count_health_services(
        self, category: Optional[str] = None, status_filter: Optional[str] = None
    ) -> int:
        """Count health services with optional filters."""
        stmt = select(func.count(HealthService.id)).where(
            HealthService.deleted_at.is_(None)
        )

        if category:
            stmt = stmt.where(HealthService.category == category)
        if status_filter:
            stmt = stmt.where(HealthService.status == status_filter)

        result = await self.db.execute(stmt)
        return result.scalar_one() or 0

    async def get_health_service(self, service_id: UUID) -> Optional[HealthService]:
        """Get a health service by ID."""
        stmt = select(HealthService).where(
            and_(
                HealthService.id == service_id,
                HealthService.deleted_at.is_(None),
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    # ========================================================================
    # Appointments
    # ========================================================================

    async def create_appointment(
        self,
        user_id: UUID,
        service_id: UUID,
        scheduled_date: datetime,
        notes: Optional[str] = None,
    ) -> Appointment:
        """Create a new appointment."""
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

    async def get_appointment(self, appointment_id: UUID) -> Optional[Appointment]:
        """Get an appointment by ID (excluding soft-deleted)."""
        stmt = (
            select(Appointment)
            .options(
                selectinload(Appointment.service),
                selectinload(Appointment.medical_record),
            )
            .where(
                and_(
                    Appointment.id == appointment_id,
                    Appointment.deleted_at.is_(None),
                )
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_user_appointments(
        self,
        user_id: UUID,
        status_filter: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Appointment]:
        """List appointments for a user (excluding soft-deleted)."""
        stmt = (
            select(Appointment)
            .options(
                selectinload(Appointment.service),
            )
            .where(
                and_(
                    Appointment.user_id == user_id,
                    Appointment.deleted_at.is_(None),
                )
            )
        )

        if status_filter:
            stmt = stmt.where(Appointment.status == status_filter)

        stmt = (
            stmt.offset(skip).limit(limit).order_by(Appointment.scheduled_date.desc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def count_user_appointments(
        self, user_id: UUID, status_filter: Optional[str] = None
    ) -> int:
        """Count appointments for a user."""
        stmt = select(func.count(Appointment.id)).where(
            and_(
                Appointment.user_id == user_id,
                Appointment.deleted_at.is_(None),
            )
        )

        if status_filter:
            stmt = stmt.where(Appointment.status == status_filter)

        result = await self.db.execute(stmt)
        return result.scalar_one() or 0

    async def cancel_appointment(self, appointment_id: UUID) -> Optional[Appointment]:
        """Cancel an appointment (soft delete)."""
        appointment = await self.get_appointment(appointment_id)
        if not appointment:
            return None

        appointment.status = "cancelled"
        appointment.deleted_at = datetime.utcnow()
        await self.db.commit()
        await self.db.refresh(appointment)
        return appointment

    # ========================================================================
    # Medical Records
    # ========================================================================

    async def get_medical_record_by_appointment(
        self, appointment_id: UUID
    ) -> Optional[MedicalRecord]:
        """Get medical record by appointment ID."""
        stmt = select(MedicalRecord).where(
            and_(
                MedicalRecord.appointment_id == appointment_id,
                MedicalRecord.deleted_at.is_(None),
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_medical_record(
        self,
        appointment_id: UUID,
        diagnosis: Optional[str] = None,
        treatment: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> MedicalRecord:
        """Create a new medical record."""
        medical_record = MedicalRecord(
            appointment_id=appointment_id,
            diagnosis=diagnosis,
            treatment=treatment,
            notes=notes,
        )
        self.db.add(medical_record)
        await self.db.commit()
        await self.db.refresh(medical_record)
        return medical_record


__all__ = ["HealthRepository"]
