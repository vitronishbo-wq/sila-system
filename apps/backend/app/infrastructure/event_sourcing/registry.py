"""
Event Registry - Maps event types to their classes for deserialization.
Enables proper reconstruction of specific event types from stored data.
"""

import logging

from apps.backend.app.core.events.domain_event import DomainEvent

logger = logging.getLogger(__name__)


class EventRegistry:
    """
    Registry for mapping event type strings to their implementation classes.

    Enables deserialization of persisted events to their original types.
    E.g., "CitizenCreated" -> CitizenCreated class
    """

    _registry: dict[str, type[DomainEvent]] = {}

    @classmethod
    def register(cls, event_type: str, event_class: type[DomainEvent]) -> None:
        """
        Register an event class by its type name.

        Args:
            event_type: String identifier (e.g., "CitizenCreated")
            event_class: The event class to register
        """
        cls._registry[event_type] = event_class
        logger.debug(f"Registered event type: {event_type} -> {event_class.__name__}")

    @classmethod
    def register_many(cls, events: dict[str, type[DomainEvent]]) -> None:
        """
        Register multiple event classes at once.

        Args:
            events: Dictionary mapping event type strings to classes
        """
        for event_type, event_class in events.items():
            cls.register(event_type, event_class)

    @classmethod
    def get(cls, event_type: str) -> type[DomainEvent] | None:
        """
        Get event class by type name.

        Args:
            event_type: The event type string

        Returns:
            Event class or None if not registered
        """
        return cls._registry.get(event_type)

    @classmethod
    def has(cls, event_type: str) -> bool:
        """Check if event type is registered."""
        return event_type in cls._registry

    @classmethod
    def list_registered(cls) -> dict[str, type[DomainEvent]]:
        """Get all registered event types and classes."""
        return dict(cls._registry)

    @classmethod
    def clear(cls) -> None:
        """Clear all registrations (for testing)."""
        cls._registry.clear()


def register_events() -> None:
    """
    Register all domain events for deserialization.
    Must be called during application startup.
    """
    try:
        from apps.backend.app.modules.justice.domain.events import (
            BirthRecordCertificateIssued,
            BirthRecordCreated,
            CitizenCreated,
            CitizenIdentityDocumentIssued,
            CitizenStatusChanged,
            DeathCertificateIssued,
            DeathRecorded,
            MarriageCertificateIssued,
            MarriageRecorded,
        )

        justice_events = {
            "CitizenCreated": CitizenCreated,
            "CitizenIdentityDocumentIssued": CitizenIdentityDocumentIssued,
            "CitizenStatusChanged": CitizenStatusChanged,
            "BirthRecordCreated": BirthRecordCreated,
            "BirthRecordCertificateIssued": BirthRecordCertificateIssued,
            "MarriageRecorded": MarriageRecorded,
            "MarriageCertificateIssued": MarriageCertificateIssued,
            "DeathRecorded": DeathRecorded,
            "DeathCertificateIssued": DeathCertificateIssued,
        }
        EventRegistry.register_many(justice_events)
        logger.info(f"Registered {len(justice_events)} justice domain events")
    except Exception as e:
        logger.warning(f"Failed to register justice events: {e}")
    logger.info(f"Event registry initialized with {len(EventRegistry.list_registered())} events")


__all__ = ["EventRegistry", "register_events"]
