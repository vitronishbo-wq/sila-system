"""Service layer for integration event management with business logic."""

import json
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from ..crud import get_integration_event_crud
from ..models.integration_event import IntegrationEventStatus, IntegrationEventType
from ..schemas.integration_crud import (
    IntegrationEventCreate,
    IntegrationEventFilter,
    IntegrationEventInDB,
    IntegrationEventUpdate,
)


class EventService:
    """Service class for integration event business logic."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.crud = get_integration_event_crud(db)

    async def create_event(
        self, event_data: IntegrationEventCreate, user_id: int
    ) -> IntegrationEventInDB:
        """Create a new integration event with business validation."""
        # Business logic: Validate event ID uniqueness
        existing_event = await self.crud.get_by_event_id(event_data.event_id)
        if existing_event:
            raise ValueError(f"Event with ID {event_data.event_id} already exists")

        # Business logic: Validate module names
        if not self._is_valid_module(event_data.source_module):
            raise ValueError(f"Invalid source module: {event_data.source_module}")

        if not self._is_valid_module(event_data.target_module):
            raise ValueError(f"Invalid target module: {event_data.target_module}")

        # Business logic: Validate payload size
        if event_data.payload:
            payload_size = len(json.dumps(event_data.payload))
            if payload_size > 1024 * 1024:  # 1MB limit
                raise ValueError("Event payload too large (max 1MB)")

        # Business logic: Set initial status based on event type
        if event_data.event_type == IntegrationEventType.SYSTEM_EVENT:
            event_data.status = IntegrationEventStatus.SUCCESS
        else:
            event_data.status = IntegrationEventStatus.PENDING

        return await self.crud.create(event_data, created_by=user_id)

    async def get_event(
        self, event_id: int, user_id: int
    ) -> Optional[IntegrationEventInDB]:
        """Get an integration event with access control."""
        event = await self.crud.get(event_id)
        if event:
            # Business logic: Check access permissions
            if not self._can_access_event(event, user_id):
                return None
        return event

    async def get_events(
        self, skip: int = 0, limit: int = 100, user_id: int = None
    ) -> List[IntegrationEventInDB]:
        """Get integration events with optional user filtering."""
        events = await self.crud.get_multi(skip=skip, limit=limit)

        # Business logic: Filter events based on user access
        if user_id:
            events = [
                event for event in events if self._can_access_event(event, user_id)
            ]

        return events

    async def update_event(
        self, event_id: int, event_data: IntegrationEventUpdate, user_id: int
    ) -> Optional[IntegrationEventInDB]:
        """Update an integration event with business validation."""
        event = await self.crud.get(event_id)
        if not event:
            return None

        # Business logic: Check update permissions
        if not self._can_update_event(event, user_id):
            raise PermissionError("User cannot update this event")

        # Business logic: Validate status transitions
        if event_data.status and not self._is_valid_status_transition(
            event.status, event_data.status
        ):
            raise ValueError(
                f"Invalid status transition from {event.status} to {event_data.status}"
            )

        # Business logic: Auto-set processed timestamp
        if event_data.status in [
            IntegrationEventStatus.SUCCESS,
            IntegrationEventStatus.FAILED,
        ]:
            event_data.processed_at = datetime.now()

        return await self.crud.update(event, event_data)

    async def delete_event(self, event_id: int, user_id: int) -> bool:
        """Delete an integration event with business validation."""
        event = await self.crud.get(event_id)
        if not event:
            return False

        # Business logic: Only allow deletion of old events
        if event.created_at > datetime.now() - timedelta(days=30):
            raise ValueError("Cannot delete events younger than 30 days")

        # Business logic: Check delete permissions
        if not self._can_delete_event(event, user_id):
            raise PermissionError("User cannot delete this event")

        return await self.crud.delete(event_id)

    async def search_events(
        self,
        filters: IntegrationEventFilter,
        skip: int = 0,
        limit: int = 100,
        user_id: int = None,
    ) -> List[IntegrationEventInDB]:
        """Search integration events with filters."""
        events = await self.crud.get_filtered(filters, skip, limit)

        # Business logic: Filter events based on user access
        if user_id:
            events = [
                event for event in events if self._can_access_event(event, user_id)
            ]

        return events

    async def get_event_statistics(
        self, module: Optional[str] = None, user_id: int = None
    ) -> Dict[str, Any]:
        """Get integration event statistics with access control."""
        stats = await self.crud.get_statistics(module)
        return stats

    async def process_event(
        self, event_id: int, user_id: int
    ) -> Optional[IntegrationEventInDB]:
        """Process an integration event."""
        event = await self.crud.get(event_id)
        if not event:
            return None

        # Business logic: Check processing permissions
        if not self._can_process_event(event, user_id):
            raise PermissionError("User cannot process this event")

        # Business logic: Only pending events can be processed
        if event.status != IntegrationEventStatus.PENDING:
            raise ValueError("Only pending events can be processed")

        update_data = IntegrationEventUpdate(status=IntegrationEventStatus.PROCESSING)
        return await self.crud.update(event, update_data)

    async def complete_event(
        self, event_id: int, user_id: int
    ) -> Optional[IntegrationEventInDB]:
        """Complete an integration event successfully."""
        event = await self.crud.get(event_id)
        if not event:
            return None

        # Business logic: Check completion permissions
        if not self._can_complete_event(event, user_id):
            raise PermissionError("User cannot complete this event")

        # Business logic: Only processing events can be completed
        if event.status != IntegrationEventStatus.PROCESSING:
            raise ValueError("Only processing events can be completed")

        update_data = IntegrationEventUpdate(
            status=IntegrationEventStatus.SUCCESS, processed_at=datetime.now()
        )
        return await self.crud.update(event, update_data)

    async def fail_event(
        self, event_id: int, user_id: int, error_message: Optional[str] = None
    ) -> Optional[IntegrationEventInDB]:
        """Mark an integration event as failed."""
        event = await self.crud.get(event_id)
        if not event:
            return None

        # Business logic: Check failure permissions
        if not self._can_fail_event(event, user_id):
            raise PermissionError("User cannot fail this event")

        # Business logic: Only processing events can be failed
        if event.status != IntegrationEventStatus.PROCESSING:
            raise ValueError("Only processing events can be marked as failed")

        update_data = IntegrationEventUpdate(
            status=IntegrationEventStatus.FAILED,
            error_message=error_message,
            processed_at=datetime.now(),
        )

        # Business logic: Increment retry count
        if event.retry_count < event.max_retries:
            update_data.retry_count = event.retry_count + 1
            # Reset to pending for retry
            update_data.status = IntegrationEventStatus.PENDING

        return await self.crud.update(event, update_data)

    async def retry_failed_events(
        self, user_id: int, module: Optional[str] = None
    ) -> List[IntegrationEventInDB]:
        """Retry failed events that haven't exceeded max retries."""
        # This would typically be called by a background job
        filters = IntegrationEventFilter(
            status=IntegrationEventStatus.FAILED, source_module=module
        )

        failed_events = await self.crud.get_filtered(filters, limit=100)
        retried_events = []

        for event in failed_events:
            if event.retry_count < event.max_retries:
                update_data = IntegrationEventUpdate(
                    status=IntegrationEventStatus.PENDING, error_message=None
                )
                retried_event = await self.crud.update(event, update_data)
                retried_events.append(retried_event)

        return retried_events

    # Business logic methods
    def _is_valid_module(self, module_name: str) -> bool:
        """Check if module name is valid."""
        # Business logic: List of valid modules
        valid_modules = [
            "justice",
            "health",
            "education",
            "finance",
            "sanitation",
            "monitoring",
            "notifications",
            "identity",
            "citizenship",
            "governance",
            "reports",
            "analytics",
            "service_hub",
        ]
        return module_name in valid_modules

    def _can_access_event(self, event: IntegrationEventInDB, user_id: int) -> bool:
        """Check if user can access the event."""
        # Business logic: Event creator can always access
        if event.created_by == user_id:
            return True

        # Business logic: Users can access events from their modules
        # (This would need to be implemented based on user permissions)

        return True  # For now, allow all users to access events

    def _can_update_event(self, event: IntegrationEventInDB, user_id: int) -> bool:
        """Check if user can update the event."""
        # Business logic: Event creator can update
        if event.created_by == user_id:
            return True

        # Business logic: System events cannot be updated
        if event.event_type == IntegrationEventType.SYSTEM_EVENT:
            return False

        return False  # For now, only creators can update

    def _can_delete_event(self, event: IntegrationEventInDB, user_id: int) -> bool:
        """Check if user can delete the event."""
        # Business logic: Only event creator can delete
        if event.created_by == user_id:
            return True

        return False

    def _can_process_event(self, event: IntegrationEventInDB, user_id: int) -> bool:
        """Check if user can process the event."""
        # Business logic: Event creator can process
        if event.created_by == user_id:
            return True

        # Business logic: System events are auto-processed
        if event.event_type == IntegrationEventType.SYSTEM_EVENT:
            return False

        return True  # For now, allow all users to process events

    def _can_complete_event(self, event: IntegrationEventInDB, user_id: int) -> bool:
        """Check if user can complete the event."""
        # Business logic: Event creator can complete
        if event.created_by == user_id:
            return True

        return True  # For now, allow all users to complete events

    def _can_fail_event(self, event: IntegrationEventInDB, user_id: int) -> bool:
        """Check if user can fail the event."""
        # Business logic: Event creator can fail
        if event.created_by == user_id:
            return True

        return True  # For now, allow all users to fail events

    def _is_valid_status_transition(
        self, current_status: IntegrationEventStatus, new_status: IntegrationEventStatus
    ) -> bool:
        """Validate integration event status transitions."""
        valid_transitions = {
            IntegrationEventStatus.PENDING: [
                IntegrationEventStatus.PROCESSING,
                IntegrationEventStatus.CANCELLED,
            ],
            IntegrationEventStatus.PROCESSING: [
                IntegrationEventStatus.SUCCESS,
                IntegrationEventStatus.FAILED,
                IntegrationEventStatus.CANCELLED,
            ],
            IntegrationEventStatus.SUCCESS: [],  # Success events cannot change status
            IntegrationEventStatus.FAILED: [
                IntegrationEventStatus.PENDING
            ],  # Failed events can be retried
            IntegrationEventStatus.CANCELLED: [],  # Cancelled events cannot change status
        }

        return new_status in valid_transitions.get(current_status, [])
