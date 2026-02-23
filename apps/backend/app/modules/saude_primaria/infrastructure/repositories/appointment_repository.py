"""Appointment Repository Implementation"""
from typing import List, Optional
from uuid import UUID
from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func

from app.modules.saude_primaria.domain.models.appointment import Appointment
from app.modules.saude_primaria.application.ports.appointment_repository_port import AppointmentRepositoryPort
from app.modules.saude_primaria.infrastructure.models.appointment_model import AppointmentModel
from app.modules.saude_primaria.domain.enums import AppointmentStatus


class AppointmentRepository(AppointmentRepositoryPort):
    """Appointment repository implementation"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    def _to_domain(self, model: AppointmentModel) -> Appointment:
        """Convert model to domain"""
        return Appointment(
            id=model.id,
            appointment_number=model.appointment_number,
            citizen_id=model.citizen_id,
            created_by=model.created_by,
            doctor_id=model.doctor_id,
            health_unit_id=model.health_unit_id,
            appointment_type=model.appointment_type,
            specialty=model.specialty,
            appointment_date=model.appointment_date,
            appointment_time=model.appointment_time,
            duration_minutes=model.duration_minutes,
            status=AppointmentStatus(model.status),
            priority=model.priority,
            reason=model.reason,
            symptoms=model.symptoms,
            notes=model.notes,
            workflow_instance_id=model.workflow_instance_id,
            workflow_data=model.workflow_data,
            metadata=model.metadata_,
            tags=model.tags,
            created_at=model.created_at,
            updated_at=model.updated_at,
            confirmed_at=model.confirmed_at,
            completed_at=model.completed_at,
            cancelled_at=model.cancelled_at,
            cancelled_reason=model.cancelled_reason
        )
    
    def _to_model(self, appointment: Appointment) -> AppointmentModel:
        """Convert domain to model"""
        return AppointmentModel(
            id=appointment.id,
            appointment_number=appointment.appointment_number,
            citizen_id=appointment.citizen_id,
            created_by=appointment.created_by,
            doctor_id=appointment.doctor_id,
            health_unit_id=appointment.health_unit_id,
            appointment_type=appointment.appointment_type.value,
            specialty=appointment.specialty,
            appointment_date=appointment.appointment_date,
            appointment_time=appointment.appointment_time,
            duration_minutes=appointment.duration_minutes,
            status=appointment.status.value,
            priority=appointment.priority.value,
            reason=appointment.reason,
            symptoms=appointment.symptoms,
            notes=appointment.notes,
            workflow_instance_id=appointment.workflow_instance_id,
            workflow_data=appointment.workflow_data,
            metadata_=appointment.metadata,
            tags=appointment.tags,
            created_at=appointment.created_at,
            updated_at=appointment.updated_at,
            confirmed_at=appointment.confirmed_at,
            completed_at=appointment.completed_at,
            cancelled_at=appointment.cancelled_at,
            cancelled_reason=appointment.cancelled_reason
        )
    
    async def save(self, appointment: Appointment) -> Appointment:
        """Save appointment"""
        model = self._to_model(appointment)
        self.db.add(model)
        await self.db.flush()
        await self.db.refresh(model)
        return self._to_domain(model)
    
    async def get_by_id(self, appointment_id: UUID) -> Optional[Appointment]:
        """Get appointment by ID"""
        stmt = select(AppointmentModel).where(AppointmentModel.id == appointment_id)
        result = await self.db.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None
    
    async def get_by_citizen(self, citizen_id: UUID, skip: int = 0, limit: int = 100) -> List[Appointment]:
        """Get appointments by citizen"""
        stmt = select(AppointmentModel).where(AppointmentModel.citizen_id == citizen_id).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]
    
    async def get_by_doctor(self, doctor_id: UUID, skip: int = 0, limit: int = 100) -> List[Appointment]:
        """Get appointments by doctor"""
        stmt = select(AppointmentModel).where(AppointmentModel.doctor_id == doctor_id).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]
    
    async def get_by_health_unit(self, health_unit_id: UUID, appointment_date: Optional[date] = None) -> List[Appointment]:
        """Get appointments by health unit"""
        query = [AppointmentModel.health_unit_id == health_unit_id]
        if appointment_date:
            query.append(AppointmentModel.appointment_date == appointment_date)
        
        stmt = select(AppointmentModel).where(and_(*query))
        result = await self.db.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]
    
    async def get_by_status(self, status: str, skip: int = 0, limit: int = 100) -> List[Appointment]:
        """Get appointments by status"""
        stmt = select(AppointmentModel).where(AppointmentModel.status == status).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]
    
    async def get_pending_confirmations(self, health_unit_id: UUID) -> List[Appointment]:
        """Get pending confirmation appointments"""
        stmt = select(AppointmentModel).where(
            and_(
                AppointmentModel.health_unit_id == health_unit_id,
                AppointmentModel.status == AppointmentStatus.SCHEDULED.value
            )
        )
        result = await self.db.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]
    
    async def get_today_schedule(self, health_unit_id: UUID) -> List[Appointment]:
        """Get today's schedule"""
        from datetime import date as date_class
        today = date_class.today()
        stmt = select(AppointmentModel).where(
            and_(
                AppointmentModel.health_unit_id == health_unit_id,
                AppointmentModel.appointment_date == today
            )
        ).order_by(AppointmentModel.appointment_time)
        result = await self.db.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]
    
    async def search(self, filters: dict, skip: int = 0, limit: int = 100) -> tuple[List[Appointment], int]:
        """Search appointments"""
        query = []
        
        if "citizen_id" in filters:
            query.append(AppointmentModel.citizen_id == filters["citizen_id"])
        if "doctor_id" in filters:
            query.append(AppointmentModel.doctor_id == filters["doctor_id"])
        if "health_unit_id" in filters:
            query.append(AppointmentModel.health_unit_id == filters["health_unit_id"])
        if "status" in filters:
            query.append(AppointmentModel.status == filters["status"])
        if "appointment_type" in filters:
            query.append(AppointmentModel.appointment_type == filters["appointment_type"])
        
        stmt = select(AppointmentModel)
        if query:
            stmt = stmt.where(and_(*query))
        
        # Get count
        count_stmt = select(func.count()).select_from(AppointmentModel)
        if query:
            count_stmt = count_stmt.where(and_(*query))
        count_result = await self.db.execute(count_stmt)
        total = count_result.scalar()
        
        stmt = stmt.offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        appointments = [self._to_domain(m) for m in result.scalars().all()]
        
        return appointments, total
    
    async def update(self, appointment: Appointment) -> Appointment:
        """Update appointment"""
        stmt = select(AppointmentModel).where(AppointmentModel.id == appointment.id)
        result = await self.db.execute(stmt)
        model = result.scalar_one()
        
        model.status = appointment.status.value
        model.priority = appointment.priority.value
        model.doctor_id = appointment.doctor_id
        model.confirmed_at = appointment.confirmed_at
        model.completed_at = appointment.completed_at
        model.cancelled_at = appointment.cancelled_at
        model.cancelled_reason = appointment.cancelled_reason
        model.appointment_date = appointment.appointment_date
        model.appointment_time = appointment.appointment_time
        model.updated_at = appointment.updated_at
        model.metadata_ = appointment.metadata
        model.workflow_data = appointment.workflow_data
        
        await self.db.flush()
        await self.db.refresh(model)
        return self._to_domain(model)
    
    async def delete(self, appointment_id: UUID) -> bool:
        """Delete appointment"""
        stmt = select(AppointmentModel).where(AppointmentModel.id == appointment_id)
        result = await self.db.execute(stmt)
        model = result.scalar_one_or_none()
        
        if model:
            await self.db.delete(model)
            await self.db.flush()
            return True
        return False
