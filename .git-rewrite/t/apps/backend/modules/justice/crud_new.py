"""CRUD operations for justice module with standardized data access."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..models.case import Case, CaseStatus
from ..models.case_event import CaseEvent, EventStatus
from ..schemas.justice_crud import (
    CaseCreate,
    CaseEventCreate,
    CaseEventInDB,
    CaseEventUpdate,
    CaseFilter,
    CaseInDB,
    CaseUpdate,
)


class CaseCRUD:
    """CRUD operations for legal cases."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, obj_in: CaseCreate, created_by: int) -> CaseInDB:
        """Create a new legal case."""
        # Generate unique case number if not provided
        if not obj_in.case_number:
            year = datetime.now().year
            count = await self.db.scalar(
                select(func.count(Case.id)).where(
                    func.extract("year", Case.filing_date) == year
                )
            )
            obj_in.case_number = f"CASE-{year}-{(count or 0) + 1:06d}"

        db_obj = Case(**obj_in.model_dump(), created_by=created_by)
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return CaseInDB.model_validate(db_obj)

    async def get(self, case_id: int) -> Optional[CaseInDB]:
        """Get a case by ID."""
        result = await self.db.execute(
            select(Case)
            .options(selectinload(Case.events), selectinload(Case.documents))
            .where(Case.id == case_id)
        )
        db_obj = result.scalar_one_or_none()
        return CaseInDB.model_validate(db_obj) if db_obj else None

    async def get_by_number(self, case_number: str) -> Optional[CaseInDB]:
        """Get a case by case number."""
        result = await self.db.execute(
            select(Case)
            .options(selectinload(Case.events), selectinload(Case.documents))
            .where(Case.case_number == case_number)
        )
        db_obj = result.scalar_one_or_none()
        return CaseInDB.model_validate(db_obj) if db_obj else None

    async def get_multi(self, skip: int = 0, limit: int = 100) -> List[CaseInDB]:
        """Get multiple cases."""
        result = await self.db.execute(
            select(Case)
            .options(selectinload(Case.events))
            .offset(skip)
            .limit(limit)
            .order_by(Case.created_at.desc())
        )
        db_objs = result.scalars().all()
        return [CaseInDB.model_validate(obj) for obj in db_objs]

    async def get_filtered(
        self, filters: CaseFilter, skip: int = 0, limit: int = 100
    ) -> List[CaseInDB]:
        """Get cases with filters."""
        query = select(Case).options(selectinload(Case.events))

        if filters.case_type:
            query = query.where(Case.case_type == filters.case_type)
        if filters.status:
            query = query.where(Case.status == filters.status)
        if filters.priority:
            query = query.where(Case.priority == filters.priority)
        if filters.court_id:
            query = query.where(Case.court_id == filters.court_id)
        if filters.created_by:
            query = query.where(Case.created_by == filters.created_by)
        if filters.is_active is not None:
            if filters.is_active:
                query = query.where(
                    Case.status.in_([CaseStatus.REGISTERED, CaseStatus.IN_PROGRESS])
                )
            else:
                query = query.where(
                    Case.status.notin_([CaseStatus.REGISTERED, CaseStatus.IN_PROGRESS])
                )

        result = await self.db.execute(
            query.offset(skip).limit(limit).order_by(Case.created_at.desc())
        )
        db_objs = result.scalars().all()
        return [CaseInDB.model_validate(obj) for obj in db_objs]

    async def update(self, db_obj: Case, obj_in: CaseUpdate) -> CaseInDB:
        """Update a case."""
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return CaseInDB.model_validate(db_obj)

    async def delete(self, case_id: int) -> bool:
        """Delete a case."""
        result = await self.db.execute(select(Case).where(Case.id == case_id))
        db_obj = result.scalar_one_or_none()
        if db_obj:
            await self.db.delete(db_obj)
            await self.db.commit()
            return True
        return False

    async def get_statistics(self, court_id: Optional[int] = None) -> Dict[str, Any]:
        """Get case statistics."""
        base_query = select(Case)
        if court_id:
            base_query = base_query.where(Case.court_id == court_id)

        total_cases = await self.db.scalar(
            select(func.count()).select_from(base_query.subquery())
        )

        active_cases = await self.db.scalar(
            select(func.count()).select_from(
                base_query.where(
                    Case.status.in_([CaseStatus.REGISTERED, CaseStatus.IN_PROGRESS])
                ).subquery()
            )
        )

        concluded_cases = await self.db.scalar(
            select(func.count()).select_from(
                base_query.where(Case.status == CaseStatus.CONCLUDED).subquery()
            )
        )

        return {
            "total_cases": total_cases or 0,
            "active_cases": active_cases or 0,
            "concluded_cases": concluded_cases or 0,
            "pending_cases": (total_cases or 0)
            - (active_cases or 0)
            - (concluded_cases or 0),
        }


class CaseEventCRUD:
    """CRUD operations for case events."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, obj_in: CaseEventCreate, created_by: int) -> CaseEventInDB:
        """Create a new case event."""
        db_obj = CaseEvent(**obj_in.model_dump(), created_by=created_by)
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return CaseEventInDB.model_validate(db_obj)

    async def get(self, event_id: int) -> Optional[CaseEventInDB]:
        """Get a case event by ID."""
        result = await self.db.execute(
            select(CaseEvent)
            .options(selectinload(CaseEvent.case))
            .where(CaseEvent.id == event_id)
        )
        db_obj = result.scalar_one_or_none()
        return CaseEventInDB.model_validate(db_obj) if db_obj else None

    async def get_by_case(
        self, case_id: int, skip: int = 0, limit: int = 100
    ) -> List[CaseEventInDB]:
        """Get events for a specific case."""
        result = await self.db.execute(
            select(CaseEvent)
            .where(CaseEvent.case_id == case_id)
            .offset(skip)
            .limit(limit)
            .order_by(CaseEvent.event_date.desc())
        )
        db_objs = result.scalars().all()
        return [CaseEventInDB.model_validate(obj) for obj in db_objs]

    async def get_multi(self, skip: int = 0, limit: int = 100) -> List[CaseEventInDB]:
        """Get multiple case events."""
        result = await self.db.execute(
            select(CaseEvent)
            .offset(skip)
            .limit(limit)
            .order_by(CaseEvent.created_at.desc())
        )
        db_objs = result.scalars().all()
        return [CaseEventInDB.model_validate(obj) for obj in db_objs]

    async def update(self, db_obj: CaseEvent, obj_in: CaseEventUpdate) -> CaseEventInDB:
        """Update a case event."""
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return CaseEventInDB.model_validate(db_obj)

    async def delete(self, event_id: int) -> bool:
        """Delete a case event."""
        result = await self.db.execute(
            select(CaseEvent).where(CaseEvent.id == event_id)
        )
        db_obj = result.scalar_one_or_none()
        if db_obj:
            await self.db.delete(db_obj)
            await self.db.commit()
            return True
        return False

    async def get_statistics(self, court_id: Optional[int] = None) -> Dict[str, Any]:
        """Get event statistics."""
        base_query = select(CaseEvent)
        if court_id:
            base_query = base_query.join(Case).where(Case.court_id == court_id)

        total_events = await self.db.scalar(
            select(func.count()).select_from(base_query.subquery())
        )

        completed_events = await self.db.scalar(
            select(func.count()).select_from(
                base_query.where(CaseEvent.status == EventStatus.COMPLETED).subquery()
            )
        )

        scheduled_events = await self.db.scalar(
            select(func.count()).select_from(
                base_query.where(CaseEvent.status == EventStatus.SCHEDULED).subquery()
            )
        )

        return {
            "total_events": total_events or 0,
            "completed_events": completed_events or 0,
            "scheduled_events": scheduled_events or 0,
            "pending_events": (total_events or 0)
            - (completed_events or 0)
            - (scheduled_events or 0),
        }


# Factory functions for dependency injection
def get_case_crud(db: AsyncSession) -> CaseCRUD:
    """Get CaseCRUD instance."""
    return CaseCRUD(db)


def get_case_event_crud(db: AsyncSession) -> CaseEventCRUD:
    """Get CaseEventCRUD instance."""
    return CaseEventCRUD(db)
