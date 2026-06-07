"""
Event Store Factory and Dependency Injection
Provides the correct EventStore implementation based on configuration
"""

import os

from apps.backend.app.infrastructure.event_sourcing.event_store import EventStore, InMemoryEventStore
from apps.backend.app.infrastructure.event_sourcing.postgres_event_store import PostgreSQLEventStore


class EventStoreFactory:
    """
    Factory for creating the appropriate EventStore implementation.

    Environment Variables:
    - EVENT_STORE_TYPE: 'memory' (default) or 'postgres'
    - ENABLE_POSTGRES_EVENTS: 'true' or 'false' (default: false)
    """

    _instance: EventStore | None = None

    @classmethod
    def get_event_store(cls, session_factory=None) -> EventStore:
        """
        Get or create the configured event store instance.

        Args:
            session_factory: SQLAlchemy async_sessionmaker (required for PostgreSQL)

        Returns:
            EventStore implementation (InMemory or PostgreSQL)
        """
        event_store_type = os.getenv("EVENT_STORE_TYPE", "memory").lower()
        enable_postgres = os.getenv("ENABLE_POSTGRES_EVENTS", "false").lower() == "true"
        if event_store_type == "postgres" or enable_postgres:
            if session_factory is None:
                raise ValueError("session_factory required for PostgreSQL EventStore")
            return PostgreSQLEventStore(session_factory)
        else:
            return InMemoryEventStore()

    @classmethod
    def reset(cls):
        """Reset the singleton instance (for testing)."""
        cls._instance = None


def get_event_store(session_factory=None) -> EventStore:
    """
    Dependency injection function for FastAPI.

    Usage in routes:
        @router.get("/events")
        async def get_events(event_store: EventStore = Depends(get_event_store)):
            events = await event_store.get_all_events()
            return events

    Args:
        session_factory: Injected AsyncSession factory

    Returns:
        EventStore instance
    """
    return EventStoreFactory.get_event_store(session_factory)


__all__ = ["EventStoreFactory", "get_event_store"]
