"""
PostgreSQL EventStore - Production-grade event persistence
Uses SQLAlchemy ORM for database abstraction
"""

import json
import logging
from datetime import date, datetime
from uuid import UUID

from apps.backend.app.core.events.domain_event import DomainEvent
from apps.backend.app.infrastructure.event_sourcing.event_store import EventStore
from apps.backend.app.infrastructure.event_sourcing.postgres_models import StoredEvent
from apps.backend.app.infrastructure.event_sourcing.registry import EventRegistry
from sqlalchemy import and_, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


class EventJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles date and datetime objects."""

    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        if isinstance(obj, UUID):
            return str(obj)
        return super().default(obj)


logger = logging.getLogger(__name__)


class EventStoreError(Exception):
    """Base exception for EventStore errors"""

    pass


class PostgreSQLEventStore(EventStore):
    """
    Production-grade event store backed by PostgreSQL.

    Features:
    - Full event persistence with audit trail
    - Atomic multi-event transactions
    - Efficient queries by aggregate, event type, or date range
    - Automatic indexing for common patterns
    - ACID compliance via PostgreSQL

    Usage:
        event_store = PostgreSQLEventStore(async_session_factory)
        await event_store.append(event)
        events = await event_store.get_events_for_aggregate(citizen_id)
    """

    def __init__(self, session_factory):
        """
        Initialize PostgreSQL EventStore.

        Args:
            session_factory: SQLAlchemy async_sessionmaker
        """
        self.session_factory = session_factory
        self.logger = logger

    async def _get_session(self) -> AsyncSession:
        """Get a new database session."""
        async with self.session_factory() as session:
            yield session

    async def append(self, event: DomainEvent) -> None:
        """
        Append a single event to the store.

        Args:
            event: DomainEvent to persist

        Raises:
            EventStoreError: If append fails
        """
        try:
            async with self.session_factory() as session:
                stored_event = StoredEvent()
                stored_event.event_id = event.event_id
                stored_event.aggregate_id = event.aggregate_id
                stored_event.aggregate_type = event.aggregate_type
                stored_event.event_type = event.event_type
                stored_event.version = event.version
                stored_event.timestamp = event.timestamp
                stored_event.event_data = json.dumps(event.to_dict(), cls=EventJSONEncoder)
                stored_event.event_metadata = (
                    json.dumps(event.metadata, cls=EventJSONEncoder) if event.metadata else None
                )
                session.add(stored_event)
                await session.commit()
                self.logger.debug(f"✓ Event appended: {event.event_type} ({event.event_id})")
        except SQLAlchemyError as e:
            self.logger.error(f"Failed to append event: {e}")
            raise EventStoreError(f"Failed to append event: {e}") from e

    async def append_batch(self, events: list[DomainEvent]) -> None:
        """
        Atomically append multiple events.

        Guarantees:
        - All events succeed or all fail (ACID)
        - Events stored in order

        Args:
            events: List of events to persist

        Raises:
            EventStoreError: If any append fails
        """
        try:
            async with self.session_factory() as session:
                stored_events = []
                for event in events:
                    stored_event = StoredEvent()
                    stored_event.event_id = event.event_id
                    stored_event.aggregate_id = event.aggregate_id
                    stored_event.aggregate_type = event.aggregate_type
                    stored_event.event_type = event.event_type
                    stored_event.version = event.version
                    stored_event.timestamp = event.timestamp
                    stored_event.event_data = json.dumps(event.to_dict(), cls=EventJSONEncoder)
                    stored_event.event_metadata = (
                        json.dumps(event.metadata, cls=EventJSONEncoder) if event.metadata else None
                    )
                    stored_events.append(stored_event)
                session.add_all(stored_events)
                await session.commit()
                self.logger.debug(f"✓ Batch appended: {len(events)} events")
        except SQLAlchemyError as e:
            self.logger.error(f"Failed to append batch: {e}")
            raise EventStoreError(f"Failed to append batch: {e}") from e

    async def get_events_for_aggregate(
        self, aggregate_id: UUID, from_version: int = 0
    ) -> list[DomainEvent]:
        """
        Retrieve all events for a specific aggregate.

        Useful for:
        - Event replay (reconstruct aggregate state)
        - Audit trail (show history of changes)

        Args:
            aggregate_id: ID of the aggregate
            from_version: Start from specific version (0 = all)

        Returns:
            List of events in chronological order
        """
        try:
            async with self.session_factory() as session:
                stmt = (
                    select(StoredEvent)
                    .where(
                        and_(
                            StoredEvent.aggregate_id == aggregate_id,
                            StoredEvent.version >= from_version,
                        )
                    )
                    .order_by(StoredEvent.timestamp.asc())
                )
                result = await session.execute(stmt)
                stored_events = result.scalars().all()
                return [self._stored_event_to_domain_event(se) for se in stored_events]
        except SQLAlchemyError as e:
            self.logger.error(f"Failed to get events for aggregate: {e}")
            raise EventStoreError(f"Failed to get events for aggregate: {e}") from e

    async def get_events_by_type(
        self, event_type: str, from_date: datetime | None = None, to_date: datetime | None = None
    ) -> list[DomainEvent]:
        """
        Retrieve all events of a specific type.

        Useful for:
        - Compliance audits ("all CitizenIdentityDocumentIssued events")
        - Reporting ("all CitizenCreated events in March")
        - Replay ("all PaymentProcessed events")

        Args:
            event_type: Type of event to retrieve
            from_date: Optional start date filter
            to_date: Optional end date filter

        Returns:
            List of matching events in chronological order
        """
        try:
            conditions = [StoredEvent.event_type == event_type]
            if from_date:
                conditions.append(StoredEvent.timestamp >= from_date)
            if to_date:
                conditions.append(StoredEvent.timestamp <= to_date)
            async with self.session_factory() as session:
                stmt = (
                    select(StoredEvent)
                    .where(and_(*conditions) if conditions else True)
                    .order_by(StoredEvent.timestamp.asc())
                )
                result = await session.execute(stmt)
                stored_events = result.scalars().all()
                return [self._stored_event_to_domain_event(se) for se in stored_events]
        except SQLAlchemyError as e:
            self.logger.error(f"Failed to get events by type: {e}")
            raise EventStoreError(f"Failed to get events by type: {e}") from e

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
        try:
            conditions = []
            if from_date:
                conditions.append(StoredEvent.timestamp >= from_date)
            if to_date:
                conditions.append(StoredEvent.timestamp <= to_date)
            async with self.session_factory() as session:
                stmt = select(StoredEvent)
                if conditions:
                    stmt = stmt.where(and_(*conditions))
                stmt = stmt.order_by(StoredEvent.timestamp.asc()).limit(limit)
                result = await session.execute(stmt)
                stored_events = result.scalars().all()
                return [self._stored_event_to_domain_event(se) for se in stored_events]
        except SQLAlchemyError as e:
            self.logger.error(f"Failed to get all events: {e}")
            raise EventStoreError(f"Failed to get all events: {e}") from e

    async def get_event_by_id(self, event_id: UUID) -> DomainEvent | None:
        """
        Retrieve a specific event by ID.

        Args:
            event_id: UUID of the event

        Returns:
            DomainEvent or None if not found
        """
        try:
            async with self.session_factory() as session:
                stmt = select(StoredEvent).where(StoredEvent.event_id == event_id)
                result = await session.execute(stmt)
                stored_event = result.scalar_one_or_none()
                if stored_event:
                    return self._stored_event_to_domain_event(stored_event)
                return None
        except SQLAlchemyError as e:
            self.logger.error(f"Failed to get event by ID: {e}")
            raise EventStoreError(f"Failed to get event by ID: {e}") from e

    @staticmethod
    def _stored_event_to_domain_event(stored_event: StoredEvent) -> DomainEvent:
        """
        Convert StoredEvent ORM object back to DomainEvent.

        Uses EventRegistry to reconstruct the specific event type from stored data.

        Args:
            stored_event: StoredEvent ORM instance

        Returns:
            DomainEvent instance (specific type if registered, base type otherwise)
        """
        event_data = json.loads(stored_event.event_data)
        event_type = event_data.get("event_type")
        event_class = EventRegistry.get(event_type) if event_type else None
        if event_class:
            return event_class.from_dict(event_data)
        else:
            return DomainEvent.from_dict(event_data)

    async def health_check(self) -> bool:
        """
        Check if event store is healthy.

        Returns:
            True if connection is working
        """
        try:
            async with self.session_factory() as session:
                await session.execute(select(StoredEvent).limit(1))
            return True
        except Exception as e:
            self.logger.error(f"EventStore health check failed: {e}")
            return False


__all__ = ["PostgreSQLEventStore", "EventStoreError"]
