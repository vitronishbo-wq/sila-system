"""Medical Record Repository Port"""
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.modules.saude_primaria.domain.models.medical_record import MedicalRecord


class MedicalRecordRepositoryPort(ABC):
    """Port for medical record data persistence"""
    
    @abstractmethod
    async def save(self, record: MedicalRecord) -> MedicalRecord:
        """Save medical record"""
        pass
    
    @abstractmethod
    async def get_by_id(self, record_id: UUID) -> Optional[MedicalRecord]:
        """Get medical record by ID"""
        pass
    
    @abstractmethod
    async def get_by_citizen(self, citizen_id: UUID, skip: int = 0, limit: int = 100) -> List[MedicalRecord]:
        """Get medical records by citizen"""
        pass
    
    @abstractmethod
    async def get_by_appointment(self, appointment_id: UUID) -> Optional[MedicalRecord]:
        """Get medical record by appointment"""
        pass
    
    @abstractmethod
    async def get_by_doctor(self, doctor_id: UUID, skip: int = 0, limit: int = 100) -> List[MedicalRecord]:
        """Get medical records by doctor"""
        pass
    
    @abstractmethod
    async def get_by_health_unit(self, health_unit_id: UUID, skip: int = 0, limit: int = 100) -> List[MedicalRecord]:
        """Get medical records by health unit"""
        pass
    
    @abstractmethod
    async def search(self, filters: dict, skip: int = 0, limit: int = 100) -> tuple[List[MedicalRecord], int]:
        """Search medical records"""
        pass
    
    @abstractmethod
    async def update(self, record: MedicalRecord) -> MedicalRecord:
        """Update medical record"""
        pass
