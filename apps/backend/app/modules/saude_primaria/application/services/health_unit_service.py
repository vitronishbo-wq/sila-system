from app.core.observability import trace
"""Health Unit Service"""
from typing import Optional, List
from uuid import UUID

from app.modules.saude_primaria.domain.models.health_unit import HealthUnit, HealthProfessional
from app.modules.saude_primaria.application.ports.health_unit_repository_port import HealthUnitRepositoryPort


class HealthUnitService:
    """Application service for health unit management"""
    
    def __init__(self, repository: HealthUnitRepositoryPort):
        self.repository = repository
    
    @trace()
    async def create_health_unit(
        self,
        code: str,
        name: str,
        unit_type,
        province: str,
        municipality: str,
        address: str,
        commune: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        beds: int = 0,
        has_emergency: bool = False,
        has_laboratory: bool = False,
        has_pharmacy: bool = False
    ) -> HealthUnit:
        """Create new health unit"""
        unit = HealthUnit(
            code=code,
            name=name,
            unit_type=unit_type,
            province=province,
            municipality=municipality,
            address=address,
            commune=commune,
            phone=phone,
            email=email,
            beds=beds,
            has_emergency=has_emergency,
            has_laboratory=has_laboratory,
            has_pharmacy=has_pharmacy
        )
        
        return await self.repository.save_unit(unit)
    
    @trace()
    async def get_health_unit(self, unit_id: UUID) -> Optional[HealthUnit]:
        """Get health unit by ID"""
        return await self.repository.get_unit_by_id(unit_id)
    
    @trace()
    async def list_municipal_units(self, municipality: str) -> List[HealthUnit]:
        """List health units by municipality"""
        return await self.repository.get_units_by_municipality(municipality)
    
    @trace()
    async def list_active_units(self, skip: int = 0, limit: int = 100) -> List[HealthUnit]:
        """List active health units"""
        return await self.repository.get_active_units(skip, limit)
    
    @trace()
    async def add_specialty(self, unit_id: UUID, specialty: str) -> HealthUnit:
        """Add specialty to health unit"""
        unit = await self.repository.get_unit_by_id(unit_id)
        if not unit:
            raise ValueError(f"Health unit {unit_id} not found")
        
        unit.add_specialty(specialty)
        return await self.repository.update_unit(unit)
    
    @trace()
    async def register_professional(
        self,
        user_id: UUID,
        health_unit_id: UUID,
        license_number: str,
        specialization: str
    ) -> HealthProfessional:
        """Register health professional"""
        professional = HealthProfessional(
            user_id=user_id,
            health_unit_id=health_unit_id,
            license_number=license_number,
            specialization=specialization
        )
        
        return await self.repository.save_professional(professional)
    
    @trace()
    async def get_unit_professionals(self, health_unit_id: UUID) -> List[HealthProfessional]:
        """Get health unit professionals"""
        return await self.repository.get_professionals_by_unit(health_unit_id)
