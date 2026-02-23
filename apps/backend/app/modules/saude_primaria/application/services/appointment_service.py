from app.core.observability import trace
"""Appointment Service"""
from typing import Optional, List
from uuid import UUID
from datetime import date, time

from app.modules.saude_primaria.domain.models.appointment import Appointment
from app.modules.saude_primaria.domain.enums import AppointmentType, PriorityLevel
from app.modules.saude_primaria.application.ports.appointment_repository_port import AppointmentRepositoryPort


class AppointmentService:
    """Application service for appointment management"""
    
    def __init__(self, repository: AppointmentRepositoryPort):
        self.repository = repository
    
    @trace()
    async def create_appointment(
        self,
        citizen_id: UUID,
        created_by: UUID,
        health_unit_id: UUID,
        appointment_type: AppointmentType,
        specialty: str,
        appointment_date: date,
        appointment_time: time,
        reason: str,
        priority: PriorityLevel = PriorityLevel.MEDIUM,
        doctor_id: Optional[UUID] = None,
        symptoms: Optional[str] = None,
        notes: Optional[str] = None
    ) -> Appointment:
        """Create new appointment"""
        appointment = Appointment(
            citizen_id=citizen_id,
            created_by=created_by,
            health_unit_id=health_unit_id,
            appointment_type=appointment_type,
            specialty=specialty,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            reason=reason,
            priority=priority,
            doctor_id=doctor_id,
            symptoms=symptoms,
            notes=notes
        )
        
        return await self.repository.save(appointment)
    
    @trace()
    async def get_appointment(self, appointment_id: UUID) -> Optional[Appointment]:
        """Get appointment by ID"""
        return await self.repository.get_by_id(appointment_id)
    
    @trace()
    async def list_citizen_appointments(self, citizen_id: UUID, skip: int = 0, limit: int = 100) -> List[Appointment]:
        """List citizen appointments"""
        return await self.repository.get_by_citizen(citizen_id, skip, limit)
    
    @trace()
    async def list_doctor_appointments(self, doctor_id: UUID, skip: int = 0, limit: int = 100) -> List[Appointment]:
        """List doctor appointments"""
        return await self.repository.get_by_doctor(doctor_id, skip, limit)
    
    @trace()
    async def get_today_schedule(self, health_unit_id: UUID) -> List[Appointment]:
        """Get today's schedule"""
        return await self.repository.get_today_schedule(health_unit_id)
    
    @trace()
    async def confirm_appointment(self, appointment_id: UUID) -> Appointment:
        """Confirm appointment"""
        appointment = await self.repository.get_by_id(appointment_id)
        if not appointment:
            raise ValueError(f"Appointment {appointment_id} not found")
        
        appointment.confirm()
        return await self.repository.update(appointment)
    
    @trace()
    async def start_appointment(self, appointment_id: UUID) -> Appointment:
        """Start appointment"""
        appointment = await self.repository.get_by_id(appointment_id)
        if not appointment:
            raise ValueError(f"Appointment {appointment_id} not found")
        
        appointment.start()
        return await self.repository.update(appointment)
    
    @trace()
    async def complete_appointment(self, appointment_id: UUID) -> Appointment:
        """Complete appointment"""
        appointment = await self.repository.get_by_id(appointment_id)
        if not appointment:
            raise ValueError(f"Appointment {appointment_id} not found")
        
        appointment.complete()
        return await self.repository.update(appointment)
    
    @trace()
    async def cancel_appointment(self, appointment_id: UUID, reason: str, cancelled_by: UUID) -> Appointment:
        """Cancel appointment"""
        appointment = await self.repository.get_by_id(appointment_id)
        if not appointment:
            raise ValueError(f"Appointment {appointment_id} not found")
        
        appointment.cancel(reason, cancelled_by)
        return await self.repository.update(appointment)
    
    @trace()
    async def reschedule_appointment(
        self,
        appointment_id: UUID,
        new_date: date,
        new_time: time,
        rescheduled_by: UUID
    ) -> Appointment:
        """Reschedule appointment"""
        appointment = await self.repository.get_by_id(appointment_id)
        if not appointment:
            raise ValueError(f"Appointment {appointment_id} not found")
        
        appointment.reschedule(new_date, new_time, rescheduled_by)
        return await self.repository.update(appointment)
    
    @trace()
    async def assign_doctor(self, appointment_id: UUID, doctor_id: UUID, assigned_by: UUID) -> Appointment:
        """Assign doctor to appointment"""
        appointment = await self.repository.get_by_id(appointment_id)
        if not appointment:
            raise ValueError(f"Appointment {appointment_id} not found")
        
        appointment.assign_doctor(doctor_id, assigned_by)
        return await self.repository.update(appointment)
    
    @trace()
    async def mark_missed(self, appointment_id: UUID) -> Appointment:
        """Mark appointment as missed"""
        appointment = await self.repository.get_by_id(appointment_id)
        if not appointment:
            raise ValueError(f"Appointment {appointment_id} not found")
        
        appointment.mark_missed()
        return await self.repository.update(appointment)
    
    @trace()
    async def search_appointments(self, filters: dict, skip: int = 0, limit: int = 100) -> tuple[List[Appointment], int]:
        """Search appointments"""
        return await self.repository.search(filters, skip, limit)
