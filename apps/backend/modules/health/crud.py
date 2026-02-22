"""CRUD operations for health records."""

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from modules.health.models.health_record import HealthRecord
from modules.health.schemas import HealthCreate, HealthInDB, HealthUpdate


class HealthCRUD:
    """CRUD operations for health records."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, obj_in: HealthCreate) -> HealthInDB:
        """Create a new health record."""
        db_obj = HealthRecord(**obj_in.model_dump())
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return HealthInDB.model_validate(db_obj)

    async def get(self, id: int) -> Optional[HealthInDB]:
        """Get a health record by ID."""
        result = await self.db.execute(
            select(HealthRecord).where(HealthRecord.id == id)
        )
        obj = result.scalar_one_or_none()
        if obj:
            return HealthInDB.model_validate(obj)
        return None

    async def get_multi(self, skip: int = 0, limit: int = 100) -> List[HealthInDB]:
        """Get multiple health records."""
        result = await self.db.execute(select(HealthRecord).offset(skip).limit(limit))
        return [HealthInDB.model_validate(obj) for obj in result.scalars().all()]

    async def update(self, id: int, obj_in: HealthUpdate) -> Optional[HealthInDB]:
        """Update a health record."""
        result = await self.db.execute(
            select(HealthRecord).where(HealthRecord.id == id)
        )
        db_obj = result.scalar_one_or_none()
        if not db_obj:
            return None

        update_data = obj_in.model_dump(exclude_unset=True)
        for field in update_data:
            if hasattr(db_obj, field):
                setattr(db_obj, field, update_data[field])

        await self.db.commit()
        await self.db.refresh(db_obj)
        return HealthInDB.model_validate(db_obj)

    async def remove(self, id: int) -> Optional[HealthInDB]:
        """Remove a health record."""
        result = await self.db.execute(
            select(HealthRecord).where(HealthRecord.id == id)
        )
        obj = result.scalar_one_or_none()
        if obj:
            await self.db.delete(obj)
            await self.db.commit()
            return HealthInDB.model_validate(obj)
        return None
