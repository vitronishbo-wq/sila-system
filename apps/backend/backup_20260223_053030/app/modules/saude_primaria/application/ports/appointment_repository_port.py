"""Appointment Repository Port"""
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from datetime import date

from app.modules.saude_primaria.domain.models.appointment import Appointment


class AppointmentRepositoryPort(ABC):
    """Port for appointment data persistence"""
    
    @abstractmethod
    async def save(self, appointment: Appointment) -> Appointment:
        """Save appointment"""
        pass
    
    @abstractmethod
    async def get_by_id(self, appointment_id: UUID) -> Optional[Appointment]:
        """Get appointment by ID"""
        pass
    
    @abstractmethod
    async def get_by_citizen(self, citizen_id: UUID, skip: int = 0, limit: int = 100) -> List[Appointment]:
        """Get appointments by citizen"""
        pass
    
    @abstractmethod
    async def get_by_doctor(self, doctor_id: UUID, skip: int = 0, limit: int = 100) -> List[Appointment]:
        """Get appointments by doctor"""
        pass
    
    @abstractmethod
    async def get_by_health_unit(self, health_unit_id: UUID, appointment_date: Optional[date] = None) -> List[Appointment]:
        """Get appointments by health unit"""
        pass
    
    @abstractmethod
    async def get_by_status(self, status: str, skip: int = 0, limit: int = 100) -> List[Appointment]:
        """Get appointments by status"""
        pass
    
    @abstractmethod
    async def get_pending_confirmations(self, health_unit_id: UUID) -> List[Appointment]:
        """Get pending confirmation appointments"""
        pass
    
    @abstractmethod
    async def get_today_schedule(self, health_unit_id: UUID) -> List[Appointment]:
        """Get today's schedule"""
        pass
    
    @abstractmethod
    async def search(self, filters: dict, skip: int = 0, limit: int = 100) -> tuple[List[Appointment], int]:
        """Search appointments with filters"""
        pass
    
    @abstractmethod
    async def update(self, appointment: Appointment) -> Appointment:
        """Update appointment"""
        pass
    
    @abstractmethod
    async def delete(self, appointment_id: UUID) -> bool:
        """Delete appointment"""
        pass
