"""Health service module."""

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from modules.health.models.health_record import HealthRecord
from modules.health.schemas import HealthCreate, HealthInDB, HealthUpdate


class HealthService:
    """Service for managing health records."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_health_record(self, health: HealthCreate) -> HealthInDB:
        """Create a new health record."""
        db_health = HealthRecord(**health.model_dump())
        self.db.add(db_health)
        await self.db.commit()
        await self.db.refresh(db_health)
        return HealthInDB.model_validate(db_health)

    async def get_health_record(self, record_id: int) -> Optional[HealthInDB]:
        """Get a health record by ID."""
        result = await self.db.execute(
            select(HealthRecord).where(HealthRecord.id == record_id)
        )
        record = result.scalar_one_or_none()
        if record:
            return HealthInDB.model_validate(record)
        return None

    async def get_health_records(
        self, skip: int = 0, limit: int = 100
    ) -> List[HealthInDB]:
        """Get a list of health records."""
        result = await self.db.execute(select(HealthRecord).offset(skip).limit(limit))
        records = result.scalars().all()
        return [HealthInDB.model_validate(record) for record in records]

    async def update_health_record(
        self, record_id: int, health: HealthUpdate
    ) -> Optional[HealthInDB]:
        """Update a health record."""
        result = await self.db.execute(
            select(HealthRecord).where(HealthRecord.id == record_id)
        )
        record = result.scalar_one_or_none()
        if not record:
            return None

        # Update fields
        for field, value in health.model_dump(exclude_unset=True).items():
            setattr(record, field, value)

        await self.db.commit()
        await self.db.refresh(record)
        return HealthInDB.model_validate(record)

    async def delete_health_record(self, record_id: int) -> bool:
        """Delete a health record."""
        result = await self.db.execute(
            select(HealthRecord).where(HealthRecord.id == record_id)
        )
        record = result.scalar_one_or_none()
        if not record:
            return False

        await self.db.delete(record)
        await self.db.commit()
        return True
