"""Health service module."""

from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from modules.health.schemas import HealthBase, HealthCreate, HealthInDB, HealthUpdate


class HealthService:
    """Service for managing health records."""

    def __init__(self, db: AsyncSession):
        """Initialize the service."""
        self.db = db

    async def get_health_info(self, id: int) -> Optional[HealthInDB]:
        """Get health info by ID."""
        result = await self.db.execute(select(HealthInDB).where(HealthInDB.id == id))
        return result.scalars().first()

    async def get_health_records(
        self, skip: int = 0, limit: int = 100
    ) -> List[HealthInDB]:
        """Get a list of health records."""
        result = await self.db.execute(select(HealthInDB).offset(skip).limit(limit))
        return result.scalars().all()

    async def create_health_record(self, health: HealthCreate) -> HealthInDB:
        """Create a new health record."""
        db_health = HealthInDB(**health.model_dump())
        self.db.add(db_health)
        await self.db.commit()
        await self.db.refresh(db_health)
        return db_health

    async def update_health_record(
        self, id: int, health: HealthUpdate
    ) -> Optional[HealthInDB]:
        """Update a health record."""
        db_health = await self.get_health_info(id)
        if db_health is None:
            return None

        for key, value in health.model_dump(exclude_unset=True).items():
            setattr(db_health, key, value)

        await self.db.commit()
        await self.db.refresh(db_health)
        return db_health

    async def delete_health_record(self, id: int) -> bool:
        """Delete a health record."""
        db_health = await self.get_health_info(id)
        if db_health is None:
            return False

        await self.db.delete(db_health)
        await self.db.commit()
        return True
