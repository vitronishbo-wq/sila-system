"""
Event Store - Persistent storage for domain events.
Implements event sourcing for audit trail and replay capabilities.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID

from apps.backend.app.core.events.domain_event import DomainEvent


class EventStore(ABC):
    """
    Abstract Event Store for persisting and retrieving domain events.

    Provides:
    - Event persistence
    - Event replay by aggregate
    - Event stream traversal
    - Compliance audit trail
    """

    @abstractmethod
    async def append(self, event: DomainEvent) -> None:
        """
        Append a single event to the store.

        Args:
            event: DomainEvent to persist

        Raises:
            EventStoreError: If append fails
        """
        pass

    @abstractmethod
    async def append_batch(self, events: list[DomainEvent]) -> None:
        """
        Atomically append multiple events.

        Args:
            events: List of events to persist
        """
        pass

    @abstractmethod
    async def get_events_for_aggregate(
        self, aggregate_id: UUID, from_version: int = 0
    ) -> list[DomainEvent]:
        """
        Retrieve all events for a specific aggregate.

        Args:
            aggregate_id: ID of the aggregate
            from_version: Start from specific version (0 = all)

        Returns:
            List of events in chronological order
        """
        pass

    @abstractmethod
    async def get_events_by_type(
        self, event_type: str, from_date: datetime | None = None, to_date: datetime | None = None
    ) -> list[DomainEvent]:
        """
        Retrieve all events of a specific type.

        Useful for:
        - Compliance audits ("all StatusChangeEvents")
        - Reporting ("all CitizenCreated events in March")
        - Replay ("all PaymentProcessed events")

        Args:
            event_type: Type of event to retrieve
            from_date: Optional start date filter
            to_date: Optional end date filter

        Returns:
            List of matching events
        """
        pass

    @abstractmethod
    async def get_all_events(
        self, from_date: datetime | None = None, to_date: datetime | None = None, limit: int = 1000
    ) -> list[DomainEvent]:
        """
        Retrieve all events (for system-wide audits).

        Args:
            from_date: Optional start date
            to_date: Optional end date
            limit: Maximum number of events to return

        Returns:
            List of all events in chronological order
        """
        pass

    @abstractmethod
    async def get_event_by_id(self, event_id: UUID) -> DomainEvent | None:
        """
        Retrieve a specific event by ID.

        Args:
            event_id: UUID of the event

        Returns:
            DomainEvent or None if not found
        """
        pass


class InMemoryEventStore(EventStore):
    """
    Simple in-memory event store for testing.
    NOT suitable for production - loses all data on restart.
    Use PostgreSQL adapter for production.
    """

    def __init__(self):
        self.events: list[DomainEvent] = []

    async def append(self, event: DomainEvent) -> None:
        """Store event in memory."""
        self.events.append(event)

    async def append_batch(self, events: list[DomainEvent]) -> None:
        """Store multiple events."""
        self.events.extend(events)

    async def get_events_for_aggregate(
        self, aggregate_id: UUID, from_version: int = 0
    ) -> list[DomainEvent]:
        """Retrieve events for an aggregate."""
        return [
            e for e in self.events if e.aggregate_id == aggregate_id and e.version >= from_version
        ]

    async def get_events_by_type(
        self, event_type: str, from_date: datetime | None = None, to_date: datetime | None = None
    ) -> list[DomainEvent]:
        """Retrieve events by type."""
        events = [e for e in self.events if e.event_type == event_type]
        if from_date:
            events = [e for e in events if e.timestamp >= from_date]
        if to_date:
            events = [e for e in events if e.timestamp <= to_date]
        return events

    async def get_all_events(
        self, from_date: datetime | None = None, to_date: datetime | None = None, limit: int = 1000
    ) -> list[DomainEvent]:
        """Retrieve all events."""
        events = self.events
        if from_date:
            events = [e for e in events if e.timestamp >= from_date]
        if to_date:
            events = [e for e in events if e.timestamp <= to_date]
        return events[:limit]

    async def get_event_by_id(self, event_id: UUID) -> DomainEvent | None:
        """Retrieve a specific event."""
        for event in self.events:
            if event.event_id == event_id:
                return event
        return None
