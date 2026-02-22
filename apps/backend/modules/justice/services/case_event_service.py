"""Service layer for case event management with business logic."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from ..crud_new import get_case_crud, get_case_event_crud
from ..models.case import CaseStatus
from ..models.case_event import EventStatus, EventType
from ..schemas.justice_crud import (
    CaseEventCreate,
    CaseEventFilter,
    CaseEventInDB,
    CaseEventUpdate,
)


class CaseEventService:
    """Service class for case event business logic."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.crud = get_case_event_crud(db)
        self.case_crud = get_case_crud(db)

    async def create_event(
        self, event_data: CaseEventCreate, user_id: int
    ) -> CaseEventInDB:
        """Create a new case event with business validation."""
        # Business logic: Validate case exists and is accessible
        case = await self.case_crud.get(event_data.case_id)
        if not case:
            raise ValueError("Case not found")

        # Business logic: Check if user can add events to this case
        if not self._can_add_event_to_case(case, user_id):
            raise PermissionError("User cannot add events to this case")

        # Business logic: Validate event date
        if event_data.event_date <= datetime.now():
            raise ValueError("Event date must be in the future")

        # Business logic: Validate event type based on case status
        if not self._is_valid_event_type_for_case(event_data.event_type, case.status):
            raise ValueError(
                f"Event type {event_data.event_type} not valid for case status {case.status}"
            )

        return await self.crud.create(event_data, created_by=user_id)

    async def get_event(self, event_id: int, user_id: int) -> Optional[CaseEventInDB]:
        """Get a case event with access control."""
        event = await self.crud.get(event_id)
        if event:
            # Business logic: Check access permissions
            if not self._can_access_event(event, user_id):
                return None
        return event

    async def get_case_events(
        self, case_id: int, skip: int = 0, limit: int = 100, user_id: int = None
    ) -> List[CaseEventInDB]:
        """Get events for a specific case with access control."""
        # Business logic: Check if user can access the case
        case = await self.case_crud.get(case_id)
        if case and user_id and not self._can_access_case(case, user_id):
            return []

        events = await self.crud.get_by_case(case_id, skip, limit)

        # Business logic: Filter events based on user access
        if user_id:
            events = [
                event for event in events if self._can_access_event(event, user_id)
            ]

        return events

    async def update_event(
        self, event_id: int, event_data: CaseEventUpdate, user_id: int
    ) -> Optional[CaseEventInDB]:
        """Update a case event with business validation."""
        event = await self.crud.get(event_id)
        if not event:
            return None

        # Business logic: Check update permissions
        if not self._can_update_event(event, user_id):
            raise PermissionError("User cannot update this event")

        # Business logic: Validate status transitions
        if event_data.status and not self._is_valid_event_status_transition(
            event.status, event_data.status
        ):
            raise ValueError(
                f"Invalid status transition from {event.status} to {event_data.status}"
            )

        # Business logic: Cannot update past events
        if event.event_date <= datetime.now() and event_data.event_date:
            raise ValueError("Cannot modify past events")

        return await self.crud.update(event, event_data)

    async def delete_event(self, event_id: int, user_id: int) -> bool:
        """Delete a case event with business validation."""
        event = await self.crud.get(event_id)
        if not event:
            return False

        # Business logic: Only allow deletion of scheduled events
        if event.status != EventStatus.SCHEDULED:
            raise ValueError("Only scheduled events can be deleted")

        # Business logic: Check delete permissions
        if not self._can_delete_event(event, user_id):
            raise PermissionError("User cannot delete this event")

        # Business logic: Cannot delete past events
        if event.event_date <= datetime.now():
            raise ValueError("Cannot delete past events")

        return await self.crud.delete(event_id)

    async def search_events(
        self,
        filters: CaseEventFilter,
        skip: int = 0,
        limit: int = 100,
        user_id: int = None,
    ) -> List[CaseEventInDB]:
        """Search events with filters."""
        events = await self.crud.get_filtered(filters, skip, limit)

        # Business logic: Filter events based on user access
        if user_id:
            events = [
                event for event in events if self._can_access_event(event, user_id)
            ]

        return events

    async def get_event_statistics(
        self, court_id: Optional[int] = None, user_id: int = None
    ) -> Dict[str, Any]:
        """Get event statistics with access control."""
        stats = await self.crud.get_statistics(court_id)

        # Business logic: Apply user-specific filtering if needed
        if user_id:
            # This would need to be implemented based on user permissions
            pass

        return stats

    async def complete_event(
        self, event_id: int, user_id: int, notes: Optional[str] = None
    ) -> Optional[CaseEventInDB]:
        """Mark an event as completed with business validation."""
        event = await self.crud.get(event_id)
        if not event:
            return None

        # Business logic: Check if event can be completed
        if event.status != EventStatus.IN_PROGRESS:
            raise ValueError("Only in-progress events can be completed")

        # Business logic: Check completion permissions
        if not self._can_complete_event(event, user_id):
            raise PermissionError("User cannot complete this event")

        update_data = CaseEventUpdate(status=EventStatus.COMPLETED)
        if notes:
            update_data.description = (
                event.description or ""
            ) + f"\n\nCompletion notes: {notes}"

        return await self.crud.update(event, update_data)

    # Business logic methods
    def _can_add_event_to_case(self, case, user_id: int) -> bool:
        """Check if user can add events to the case."""
        # Business logic: Case creator can always add events
        if hasattr(case, "created_by") and case.created_by == user_id:
            return True

        # Business logic: Additional rules would go here
        return True  # For now, allow all users to add events

    def _can_access_event(self, event, user_id: int) -> bool:
        """Check if user can access the event."""
        # Business logic: Event creator can always access
        if hasattr(event, "created_by") and event.created_by == user_id:
            return True

        # Business logic: Public events can be accessed by anyone
        if hasattr(event, "is_public") and event.is_public:
            return True

        return True  # For now, allow all users to access events

    def _can_access_case(self, case, user_id: int) -> bool:
        """Check if user can access the case."""
        # Business logic: Case creator can always access
        if hasattr(case, "created_by") and case.created_by == user_id:
            return True

        # Business logic: Public cases can be accessed by anyone
        if (
            hasattr(case, "is_public")
            and case.is_public
            and not getattr(case, "is_confidential", False)
        ):
            return True

        return True  # For now, allow all users to access cases

    def _can_update_event(self, event, user_id: int) -> bool:
        """Check if user can update the event."""
        # Business logic: Event creator can update
        if hasattr(event, "created_by") and event.created_by == user_id:
            return True

        return False  # For now, only creators can update

    def _can_delete_event(self, event, user_id: int) -> bool:
        """Check if user can delete the event."""
        # Business logic: Event creator can delete
        if hasattr(event, "created_by") and event.created_by == user_id:
            return True

        return False  # For now, only creators can delete

    def _can_complete_event(self, event, user_id: int) -> bool:
        """Check if user can complete the event."""
        # Business logic: Event creator can complete
        if hasattr(event, "created_by") and event.created_by == user_id:
            return True

        return True  # For now, allow all users to complete events

    def _is_valid_event_type_for_case(
        self, event_type: EventType, case_status: CaseStatus
    ) -> bool:
        """Validate event type based on case status."""
        # Business logic: Define valid event types for each case status
        valid_events_by_status = {
            CaseStatus.REGISTERED: [
                EventType.HEARING,
                EventType.MOTION,
                EventType.EVIDENCE_SUBMISSION,
            ],
            CaseStatus.IN_PROGRESS: [
                EventType.HEARING,
                EventType.DEPOSITION,
                EventType.RULING,
                EventType.MOTION,
                EventType.EVIDENCE_SUBMISSION,
                EventType.WITNESS_TESTIMONY,
                EventType.EXPERT_REPORT,
                EventType.MEDIATION,
                EventType.SETTLEMENT,
            ],
            CaseStatus.SUSPENDED: [EventType.POSTPONEMENT, EventType.MOTION],
            CaseStatus.CONCLUDED: [EventType.APPEAL],
            CaseStatus.APPEALED: [
                EventType.HEARING,
                EventType.MOTION,
                EventType.SENTENCE,
            ],
            CaseStatus.ARCHIVED: [],  # No events for archived cases
        }

        return event_type in valid_events_by_status.get(case_status, [])

    def _is_valid_event_status_transition(
        self, current_status: EventStatus, new_status: EventStatus
    ) -> bool:
        """Validate event status transitions."""
        valid_transitions = {
            EventStatus.SCHEDULED: [
                EventStatus.IN_PROGRESS,
                EventStatus.CANCELLED,
                EventStatus.POSTPONED,
            ],
            EventStatus.IN_PROGRESS: [
                EventStatus.COMPLETED,
                EventStatus.CANCELLED,
                EventStatus.POSTPONED,
            ],
            EventStatus.COMPLETED: [],  # Completed events cannot change status
            EventStatus.CANCELLED: [],  # Cancelled events cannot change status
            EventStatus.POSTPONED: [EventStatus.SCHEDULED, EventStatus.CANCELLED],
        }

        return new_status in valid_transitions.get(current_status, [])

    @staticmethod
    async def get_event_statistics(
        db: AsyncSession, court_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Static method for backward compatibility."""
        service = CaseEventService(db)
        return await service.get_event_statistics(court_id)
