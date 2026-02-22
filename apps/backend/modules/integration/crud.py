"""CRUD operations for integration module with standardized data access."""

from typing import Any, Dict, List, Optional
from uuid import UUID

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.integration_event import IntegrationEvent
from ..schemas.integration_crud import (
    IntegrationEventCreate,
    IntegrationEventFilter,
    IntegrationEventInDB,
    IntegrationEventUpdate,
)


class IntegrationEventCRUD:
    """CRUD operations for integration events."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self, obj_in: IntegrationEventCreate, created_by: int
    ) -> IntegrationEventInDB:
        """Create a new integration event."""
        # Generate unique event ID if not provided
        if not obj_in.event_id:
            obj_in.event_id = str(UUID.uuid4())

        db_obj = IntegrationEvent(**obj_in.model_dump(), created_by=created_by)
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return IntegrationEventInDB.model_validate(db_obj)

    async def get(self, event_id: int) -> Optional[IntegrationEventInDB]:
        """Get an integration event by ID."""
        result = await self.db.execute(
            select(IntegrationEvent).where(IntegrationEvent.id == event_id)
        )
        db_obj = result.scalar_one_or_none()
        return IntegrationEventInDB.model_validate(db_obj) if db_obj else None

    async def get_by_event_id(self, event_id: str) -> Optional[IntegrationEventInDB]:
        """Get an integration event by event ID."""
        result = await self.db.execute(
            select(IntegrationEvent).where(IntegrationEvent.event_id == event_id)
        )
        db_obj = result.scalar_one_or_none()
        return IntegrationEventInDB.model_validate(db_obj) if db_obj else None

    async def get_multi(
        self, skip: int = 0, limit: int = 100
    ) -> List[IntegrationEventInDB]:
        """Get multiple integration events."""
        result = await self.db.execute(
            select(IntegrationEvent)
            .offset(skip)
            .limit(limit)
            .order_by(IntegrationEvent.created_at.desc())
        )
        db_objs = result.scalars().all()
        return [IntegrationEventInDB.model_validate(obj) for obj in db_objs]

    async def get_filtered(
        self, filters: IntegrationEventFilter, skip: int = 0, limit: int = 100
    ) -> List[IntegrationEventInDB]:
        """Get integration events with filters."""
        query = select(IntegrationEvent)

        if filters.source_module:
            query = query.where(IntegrationEvent.source_module == filters.source_module)
        if filters.target_module:
            query = query.where(IntegrationEvent.target_module == filters.target_module)
        if filters.event_type:
            query = query.where(IntegrationEvent.event_type == filters.event_type)
        if filters.status:
            query = query.where(IntegrationEvent.status == filters.status)
        if filters.created_by:
            query = query.where(IntegrationEvent.created_by == filters.created_by)
        if filters.date_from:
            query = query.where(IntegrationEvent.created_at >= filters.date_from)
        if filters.date_to:
            query = query.where(IntegrationEvent.created_at <= filters.date_to)

        result = await self.db.execute(
            query.offset(skip).limit(limit).order_by(IntegrationEvent.created_at.desc())
        )
        db_objs = result.scalars().all()
        return [IntegrationEventInDB.model_validate(obj) for obj in db_objs]

    async def update(
        self, db_obj: IntegrationEvent, obj_in: IntegrationEventUpdate
    ) -> IntegrationEventInDB:
        """Update an integration event."""
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return IntegrationEventInDB.model_validate(db_obj)

    async def delete(self, event_id: int) -> bool:
        """Delete an integration event."""
        result = await self.db.execute(
            select(IntegrationEvent).where(IntegrationEvent.id == event_id)
        )
        db_obj = result.scalar_one_or_none()
        if db_obj:
            await self.db.delete(db_obj)
            await self.db.commit()
            return True
        return False

    async def get_statistics(self, module: Optional[str] = None) -> Dict[str, Any]:
        """Get integration event statistics."""
        base_query = select(IntegrationEvent)
        if module:
            base_query = base_query.where(
                or_(
                    IntegrationEvent.source_module == module,
                    IntegrationEvent.target_module == module,
                )
            )

        total_events = await self.db.scalar(
            select(func.count()).select_from(base_query.subquery())
        )

        successful_events = await self.db.scalar(
            select(func.count()).select_from(
                base_query.where(IntegrationEvent.status == "success").subquery()
            )
        )

        failed_events = await self.db.scalar(
            select(func.count()).select_from(
                base_query.where(IntegrationEvent.status == "failed").subquery()
            )
        )

        return {
            "total_events": total_events or 0,
            "successful_events": successful_events or 0,
            "failed_events": failed_events or 0,
            "pending_events": (total_events or 0)
            - (successful_events or 0)
            - (failed_events or 0),
        }


# Factory function for dependency injection
def get_integration_event_crud(db: AsyncSession) -> IntegrationEventCRUD:
    """Get IntegrationEventCRUD instance."""
    return IntegrationEventCRUD(db)
