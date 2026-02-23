from typing import List, Optional, Tuple
from uuid import UUID
from sqlalchemy import select, func, desc
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.saude_primaria.infrastructure.db.healthcare_model import HealthcareRequestModel

class HealthcareRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(self, model: HealthcareRequestModel) -> HealthcareRequestModel:
        """Salva ou atualiza um pedido."""
        # Find if exists
        stmt = select(HealthcareRequestModel).where(HealthcareRequestModel.id == model.id)
        result = await self.db.execute(stmt)
        existing = result.scalar_one_or_none()
        
        if existing:
            # Update attributes
            # For simplicity in this refactor, we assume the model passed is already the one in the session or a new one
            # If it's a domain object transformation, we'd do attribute mapping here.
            # In saude_primaria, it seems it uses the Model directly in the service for now.
            pass 
        else:
            self.db.add(model)
        
        await self.db.flush()
        return model

    async def get_by_id(self, request_id: UUID) -> Optional[HealthcareRequestModel]:
        stmt = select(HealthcareRequestModel).options(
            joinedload(HealthcareRequestModel.maternal_record),
            joinedload(HealthcareRequestModel.post_natal_record),
            joinedload(HealthcareRequestModel.chronic_monitoring),
            joinedload(HealthcareRequestModel.nutrition_record),
            joinedload(HealthcareRequestModel.psychology_session),
            joinedload(HealthcareRequestModel.health_alert)
        ).where(HealthcareRequestModel.id == request_id)
        
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_citizen(self, citizen_id: UUID, skip: int = 0, limit: int = 100, **filters) -> Tuple[List[HealthcareRequestModel], int]:
        # Count
        count_stmt = select(func.count()).select_from(HealthcareRequestModel).where(
            HealthcareRequestModel.citizen_id == citizen_id
        )
        count_result = await self.db.execute(count_stmt)
        total = count_result.scalar() or 0
        
        # Query
        stmt = select(HealthcareRequestModel).options(
            joinedload(HealthcareRequestModel.maternal_record),
            joinedload(HealthcareRequestModel.post_natal_record),
            joinedload(HealthcareRequestModel.chronic_monitoring),
            joinedload(HealthcareRequestModel.nutrition_record),
            joinedload(HealthcareRequestModel.psychology_session),
            joinedload(HealthcareRequestModel.health_alert)
        ).where(
            HealthcareRequestModel.citizen_id == citizen_id
        ).order_by(desc(HealthcareRequestModel.created_at)).offset(skip).limit(limit)
        
        result = await self.db.execute(stmt)
        return list(result.scalars().all()), total

    async def list_by_citizen(self, citizen_id: UUID) -> List[HealthcareRequestModel]:
        # For backward compatibility with existing service methods
        res, _ = await self.get_by_citizen(citizen_id, limit=1000)
        return res