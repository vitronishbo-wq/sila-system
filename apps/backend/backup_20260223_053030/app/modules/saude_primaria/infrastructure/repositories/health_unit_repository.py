"""Health Unit Repository Implementation"""
from typing import List, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func

from app.modules.saude_primaria.domain.models.health_unit import HealthUnit, HealthProfessional
from app.modules.saude_primaria.application.ports.health_unit_repository_port import HealthUnitRepositoryPort
from app.modules.saude_primaria.infrastructure.models.health_unit_model import HealthUnitModel, HealthProfessionalModel


class HealthUnitRepository(HealthUnitRepositoryPort):
    """Health unit repository implementation"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    def _unit_to_domain(self, model: HealthUnitModel) -> HealthUnit:
        """Convert model to domain"""
        return HealthUnit(
            id=model.id,
            code=model.code,
            name=model.name,
            unit_type=model.unit_type,
            province=model.province,
            municipality=model.municipality,
            commune=model.commune,
            address=model.address,
            phone=model.phone,
            email=model.email,
            beds=model.beds,
            has_emergency=model.has_emergency,
            has_laboratory=model.has_laboratory,
            has_pharmacy=model.has_pharmacy,
            specialties=model.specialties or [],
            opening_hours=model.opening_hours or {},
            metadata=model.metadata_,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    def _unit_to_model(self, unit: HealthUnit) -> HealthUnitModel:
        """Convert domain to model"""
        return HealthUnitModel(
            id=unit.id,
            code=unit.code,
            name=unit.name,
            unit_type=unit.unit_type.value,
            province=unit.province,
            municipality=unit.municipality,
            commune=unit.commune,
            address=unit.address,
            phone=unit.phone,
            email=unit.email,
            beds=unit.beds,
            has_emergency=unit.has_emergency,
            has_laboratory=unit.has_laboratory,
            has_pharmacy=unit.has_pharmacy,
            specialties=unit.specialties,
            opening_hours=unit.opening_hours,
            metadata_=unit.metadata,
            is_active=unit.is_active,
            created_at=unit.created_at,
            updated_at=unit.updated_at
        )
    
    def _prof_to_domain(self, model: HealthProfessionalModel) -> HealthProfessional:
        """Convert professional model to domain"""
        return HealthProfessional(
            id=model.id,
            user_id=model.user_id,
            health_unit_id=model.health_unit_id,
            license_number=model.license_number,
            specialization=model.specialization,
            metadata=model.metadata_,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    def _prof_to_model(self, professional: HealthProfessional) -> HealthProfessionalModel:
        """Convert professional domain to model"""
        return HealthProfessionalModel(
            id=professional.id,
            user_id=professional.user_id,
            health_unit_id=professional.health_unit_id,
            license_number=professional.license_number,
            specialization=professional.specialization,
            metadata_=professional.metadata,
            created_at=professional.created_at,
            updated_at=professional.updated_at
        )
    
    async def save_unit(self, unit: HealthUnit) -> HealthUnit:
        """Save health unit"""
        model = self._unit_to_model(unit)
        self.db.add(model)
        await self.db.flush()
        await self.db.refresh(model)
        return self._unit_to_domain(model)
    
    async def get_unit_by_id(self, unit_id: UUID) -> Optional[HealthUnit]:
        """Get health unit by ID"""
        stmt = select(HealthUnitModel).where(HealthUnitModel.id == unit_id)
        result = await self.db.execute(stmt)
        model = result.scalar_one_or_none()
        return self._unit_to_domain(model) if model else None
    
    async def get_units_by_municipality(self, municipality: str) -> List[HealthUnit]:
        """Get health units by municipality"""
        stmt = select(HealthUnitModel).where(HealthUnitModel.municipality == municipality)
        result = await self.db.execute(stmt)
        return [self._unit_to_domain(m) for m in result.scalars().all()]
    
    async def get_active_units(self, skip: int = 0, limit: int = 100) -> List[HealthUnit]:
        """Get active health units"""
        stmt = select(HealthUnitModel).where(HealthUnitModel.is_active == True).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return [self._unit_to_domain(m) for m in result.scalars().all()]
    
    async def get_units_by_type(self, unit_type: str) -> List[HealthUnit]:
        """Get health units by type"""
        stmt = select(HealthUnitModel).where(HealthUnitModel.unit_type == unit_type)
        result = await self.db.execute(stmt)
        return [self._unit_to_domain(m) for m in result.scalars().all()]
    
    async def search_units(self, filters: dict, skip: int = 0, limit: int = 100) -> tuple[List[HealthUnit], int]:
        """Search health units"""
        query = []
        
        if "municipality" in filters:
            query.append(HealthUnitModel.municipality == filters["municipality"])
        if "unit_type" in filters:
            query.append(HealthUnitModel.unit_type == filters["unit_type"])
        if "is_active" in filters:
            query.append(HealthUnitModel.is_active == filters["is_active"])
        
        stmt = select(HealthUnitModel)
        if query:
            stmt = stmt.where(and_(*query))
        
        count_stmt = select(func.count()).select_from(HealthUnitModel)
        if query:
            count_stmt = count_stmt.where(and_(*query))
        count_result = await self.db.execute(count_stmt)
        total = count_result.scalar()
        
        stmt = stmt.offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        units = [self._unit_to_domain(m) for m in result.scalars().all()]
        
        return units, total
    
    async def update_unit(self, unit: HealthUnit) -> HealthUnit:
        """Update health unit"""
        stmt = select(HealthUnitModel).where(HealthUnitModel.id == unit.id)
        result = await self.db.execute(stmt)
        model = result.scalar_one()
        
        model.name = unit.name
        model.specialties = unit.specialties
        model.is_active = unit.is_active
        model.opening_hours = unit.opening_hours
        model.metadata_ = unit.metadata
        model.updated_at = unit.updated_at
        
        await self.db.flush()
        await self.db.refresh(model)
        return self._unit_to_domain(model)
    
    async def save_professional(self, professional: HealthProfessional) -> HealthProfessional:
        """Save health professional"""
        model = self._prof_to_model(professional)
        self.db.add(model)
        await self.db.flush()
        await self.db.refresh(model)
        return self._prof_to_domain(model)
    
    async def get_professionals_by_unit(self, health_unit_id: UUID) -> List[HealthProfessional]:
        """Get professionals by health unit"""
        stmt = select(HealthProfessionalModel).where(HealthProfessionalModel.health_unit_id == health_unit_id)
        result = await self.db.execute(stmt)
        return [self._prof_to_domain(m) for m in result.scalars().all()]
