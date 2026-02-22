"""Prescription Repository Port"""
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.modules.saude_primaria.domain.models.prescription import Prescription


class PrescriptionRepositoryPort(ABC):
    """Port for prescription data persistence"""
    
    @abstractmethod
    async def save(self, prescription: Prescription) -> Prescription:
        """Save prescription"""
        pass
    
    @abstractmethod
    async def get_by_id(self, prescription_id: UUID) -> Optional[Prescription]:
        """Get prescription by ID"""
        pass
    
    @abstractmethod
    async def get_by_citizen(self, citizen_id: UUID, skip: int = 0, limit: int = 100) -> List[Prescription]:
        """Get prescriptions by citizen"""
        pass
    
    @abstractmethod
    async def get_by_doctor(self, doctor_id: UUID, skip: int = 0, limit: int = 100) -> List[Prescription]:
        """Get prescriptions by doctor"""
        pass
    
    @abstractmethod
    async def get_active_by_citizen(self, citizen_id: UUID) -> List[Prescription]:
        """Get active prescriptions for citizen"""
        pass
    
    @abstractmethod
    async def get_by_appointment(self, appointment_id: UUID) -> List[Prescription]:
        """Get prescriptions by appointment"""
        pass
    
    @abstractmethod
    async def get_expired(self) -> List[Prescription]:
        """Get expired prescriptions"""
        pass
    
    @abstractmethod
    async def search(self, filters: dict, skip: int = 0, limit: int = 100) -> tuple[List[Prescription], int]:
        """Search prescriptions with filters"""
        pass
    
    @abstractmethod
    async def update(self, prescription: Prescription) -> Prescription:
        """Update prescription"""
        pass
    
    @abstractmethod
    async def delete(self, prescription_id: UUID) -> bool:
        """Delete prescription"""
        pass
