"""Health Unit Repository Port"""
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.modules.saude_primaria.domain.models.health_unit import HealthUnit, HealthProfessional


class HealthUnitRepositoryPort(ABC):
    """Port for health unit data persistence"""
    
    @abstractmethod
    async def save_unit(self, unit: HealthUnit) -> HealthUnit:
        """Save health unit"""
        pass
    
    @abstractmethod
    async def get_unit_by_id(self, unit_id: UUID) -> Optional[HealthUnit]:
        """Get health unit by ID"""
        pass
    
    @abstractmethod
    async def get_units_by_municipality(self, municipality: str) -> List[HealthUnit]:
        """Get health units by municipality"""
        pass
    
    @abstractmethod
    async def get_active_units(self, skip: int = 0, limit: int = 100) -> List[HealthUnit]:
        """Get active health units"""
        pass
    
    @abstractmethod
    async def get_units_by_type(self, unit_type: str) -> List[HealthUnit]:
        """Get health units by type"""
        pass
    
    @abstractmethod
    async def search_units(self, filters: dict, skip: int = 0, limit: int = 100) -> tuple[List[HealthUnit], int]:
        """Search health units"""
        pass
    
    @abstractmethod
    async def update_unit(self, unit: HealthUnit) -> HealthUnit:
        """Update health unit"""
        pass
    
    @abstractmethod
    async def save_professional(self, professional: HealthProfessional) -> HealthProfessional:
        """Save health professional"""
        pass
    
    @abstractmethod
    async def get_professionals_by_unit(self, health_unit_id: UUID) -> List[HealthProfessional]:
        """Get professionals by health unit"""
        pass
