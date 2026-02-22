"""CRUD operations for sanitation records."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from modules.sanitation.models.sanitation import SanitationRecord, SanitationType
from modules.sanitation.schemas.sanitation import (
    SanitationCreate,
    SanitationFilter,
    SanitationInDB,
    SanitationUpdate,
)


class SanitationCRUD:
    """CRUD operations for sanitation records with standardized data access."""

    def __init__(self, db: AsyncSession):
        self.db = db

    # Standard CRUD Operations
    async def create(self, obj_in: SanitationCreate) -> SanitationInDB:
        """Create a new sanitation record."""
        db_obj = SanitationRecord(**obj_in.model_dump())
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return SanitationInDB.model_validate(db_obj)

    async def get(self, id: int) -> Optional[SanitationInDB]:
        """Get a sanitation record by ID."""
        result = await self.db.execute(
            select(SanitationRecord).where(SanitationRecord.id == id)
        )
        obj = result.scalar_one_or_none()
        if obj:
            return SanitationInDB.model_validate(obj)
        return None

    async def get_multi(
        self, skip: int = 0, limit: int = 100, municipality_id: Optional[int] = None
    ) -> List[SanitationInDB]:
        """Get multiple sanitation records with optional filtering."""
        query = select(SanitationRecord)

        if municipality_id:
            query = query.where(SanitationRecord.municipality_id == municipality_id)

        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return [SanitationInDB.model_validate(obj) for obj in result.scalars().all()]

    async def update(
        self, id: int, obj_in: SanitationUpdate
    ) -> Optional[SanitationInDB]:
        """Update a sanitation record."""
        result = await self.db.execute(
            select(SanitationRecord).where(SanitationRecord.id == id)
        )
        db_obj = result.scalar_one_or_none()
        if not db_obj:
            return None

        update_data = obj_in.model_dump(exclude_unset=True)
        for field in update_data:
            if hasattr(db_obj, field):
                setattr(db_obj, field, update_data[field])

        # Update last_updated timestamp
        db_obj.last_updated = datetime.utcnow()

        await self.db.commit()
        await self.db.refresh(db_obj)
        return SanitationInDB.model_validate(db_obj)

    async def remove(self, id: int) -> Optional[SanitationInDB]:
        """Remove a sanitation record."""
        result = await self.db.execute(
            select(SanitationRecord).where(SanitationRecord.id == id)
        )
        obj = result.scalar_one_or_none()
        if obj:
            await self.db.delete(obj)
            await self.db.commit()
            return SanitationInDB.model_validate(obj)
        return None

    # Advanced Query Operations
    async def get_by_municipality(self, municipality_id: int) -> List[SanitationInDB]:
        """Get all sanitation records for a specific municipality."""
        result = await self.db.execute(
            select(SanitationRecord).where(
                SanitationRecord.municipality_id == municipality_id
            )
        )
        return [SanitationInDB.model_validate(obj) for obj in result.scalars().all()]

    async def get_by_type(self, sanitation_type: str) -> List[SanitationInDB]:
        """Get sanitation records by type."""
        result = await self.db.execute(
            select(SanitationRecord).where(
                SanitationRecord.sanitation_type == sanitation_type
            )
        )
        return [SanitationInDB.model_validate(obj) for obj in result.scalars().all()]

    async def get_by_responsible_entity(self, entity: str) -> List[SanitationInDB]:
        """Get sanitation records by responsible entity."""
        result = await self.db.execute(
            select(SanitationRecord).where(
                SanitationRecord.responsible_entity == entity
            )
        )
        return [SanitationInDB.model_validate(obj) for obj in result.scalars().all()]

    async def search(self, filters: SanitationFilter) -> List[SanitationInDB]:
        """Search sanitation records with multiple filters."""
        query = select(SanitationRecord)

        # Build dynamic query based on filters
        if filters.municipality_id:
            query = query.where(
                SanitationRecord.municipality_id == filters.municipality_id
            )

        if filters.sanitation_type:
            query = query.where(
                SanitationRecord.sanitation_type == filters.sanitation_type
            )

        if filters.responsible_entity:
            query = query.where(
                SanitationRecord.responsible_entity.ilike(
                    f"%{filters.responsible_entity}%"
                )
            )

        if filters.technical_manager:
            query = query.where(
                SanitationRecord.technical_manager.ilike(
                    f"%{filters.technical_manager}%"
                )
            )

        if filters.min_coverage is not None:
            query = query.where(
                SanitationRecord.coverage_percentage >= filters.min_coverage
            )

        if filters.max_coverage is not None:
            query = query.where(
                SanitationRecord.coverage_percentage <= filters.max_coverage
            )

        if filters.date_from:
            query = query.where(SanitationRecord.last_updated >= filters.date_from)

        if filters.date_to:
            query = query.where(SanitationRecord.last_updated <= filters.date_to)

        # Apply pagination
        if filters.skip:
            query = query.offset(filters.skip)
        if filters.limit:
            query = query.limit(filters.limit)

        result = await self.db.execute(query)
        return [SanitationInDB.model_validate(obj) for obj in result.scalars().all()]

    # Statistics and Analytics
    async def get_statistics(
        self, municipality_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get sanitation statistics."""
        query = select(
            func.count(SanitationRecord.id).label("total_records"),
            func.avg(SanitationRecord.coverage_percentage).label("avg_coverage"),
            func.min(SanitationRecord.coverage_percentage).label("min_coverage"),
            func.max(SanitationRecord.coverage_percentage).label("max_coverage"),
        )

        if municipality_id:
            query = query.where(SanitationRecord.municipality_id == municipality_id)

        result = await self.db.execute(query)
        stats = result.first()

        return {
            "total_records": stats.total_records or 0,
            "avg_coverage": float(stats.avg_coverage or 0),
            "min_coverage": float(stats.min_coverage or 0),
            "max_coverage": float(stats.max_coverage or 0),
        }

    async def get_by_type_breakdown(
        self, municipality_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get breakdown of records by sanitation type."""
        query = select(
            SanitationRecord.sanitation_type,
            func.count(SanitationRecord.id).label("count"),
            func.avg(SanitationRecord.coverage_percentage).label("avg_coverage"),
        ).group_by(SanitationRecord.sanitation_type)

        if municipality_id:
            query = query.where(SanitationRecord.municipality_id == municipality_id)

        result = await self.db.execute(query)
        breakdown = {}

        for row in result:
            breakdown[row.sanitation_type] = {
                "count": row.count,
                "avg_coverage": float(row.avg_coverage or 0),
            }

        return breakdown

    async def get_low_coverage_records(
        self, threshold: float = 50.0
    ) -> List[SanitationInDB]:
        """Get records with coverage below threshold."""
        result = await self.db.execute(
            select(SanitationRecord).where(
                SanitationRecord.coverage_percentage < threshold
            )
        )
        return [SanitationInDB.model_validate(obj) for obj in result.scalars().all()]

    # Batch Operations
    async def create_batch(
        self, objects_in: List[SanitationCreate]
    ) -> List[SanitationInDB]:
        """Create multiple sanitation records in batch."""
        db_objects = [SanitationRecord(**obj.model_dump()) for obj in objects_in]
        self.db.add_all(db_objects)
        await self.db.commit()

        # Refresh all objects to get their IDs
        for obj in db_objects:
            await self.db.refresh(obj)

        return [SanitationInDB.model_validate(obj) for obj in db_objects]

    async def update_batch(self, updates: List[Dict[str, Any]]) -> List[SanitationInDB]:
        """Update multiple records in batch."""
        updated_objects = []

        for update_data in updates:
            record_id = update_data.pop("id", None)
            if record_id:
                updated = await self.update(record_id, SanitationUpdate(**update_data))
                if updated:
                    updated_objects.append(updated)

        return updated_objects

    async def delete_batch(self, ids: List[int]) -> List[SanitationInDB]:
        """Delete multiple records in batch."""
        deleted_objects = []

        for record_id in ids:
            deleted = await self.remove(record_id)
            if deleted:
                deleted_objects.append(deleted)

        return deleted_objects

    # SanitationType Operations
    async def get_sanitation_types(self) -> List[SanitationType]:
        """Get all available sanitation types."""
        result = await self.db.execute(select(SanitationType))
        return result.scalars().all()

    async def get_sanitation_type_by_name(self, name: str) -> Optional[SanitationType]:
        """Get sanitation type by name."""
        result = await self.db.execute(
            select(SanitationType).where(SanitationType.name == name)
        )
        return result.scalar_one_or_none()


# Factory function for dependency injection
def get_sanitation_crud(db: AsyncSession) -> SanitationCRUD:
    """Get sanitation CRUD instance."""
    return SanitationCRUD(db)


# Export CRUD instance for backward compatibility
def create_sanitation_crud(db: AsyncSession) -> SanitationCRUD:
    """Create sanitation CRUD instance (alias for get_sanitation_crud)."""
    return get_sanitation_crud(db)


__all__ = ["SanitationCRUD", "get_sanitation_crud", "create_sanitation_crud"]
