"""
Event Bus - Abstract interface for event publishing and subscription.
Supports both synchronous and asynchronous event handling.
"""

from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable

from .domain_event import DomainEvent


class EventHandler(ABC):
    """Base class for event handlers."""

    @abstractmethod
    async def handle(self, event: DomainEvent) -> None:
        """Handle a domain event."""
        pass


class EventBus(ABC):
    """
    Abstract Event Bus for publishing and subscribing to events.

    Implementations should handle:
    - Event persistence (event store)
    - Event publication (message broker)
    - Event subscription and handler dispatch
    - Error handling and retries
    """

    @abstractmethod
    async def publish(self, event: DomainEvent) -> None:
        """
        Publish an event to all subscribers.

        Args:
            event: DomainEvent to publish

        Raises:
            EventPublishError: If publication fails
        """
        pass

    @abstractmethod
    async def subscribe(
        self, event_type: str, handler: Callable[[DomainEvent], Awaitable[None]]
    ) -> None:
        """
        Subscribe a handler to a specific event type.

        Args:
            event_type: Type of event to subscribe to (e.g., "CitizenCreated")
            handler: Async callback function to handle the event
        """
        pass

    @abstractmethod
    async def unsubscribe(
        self, event_type: str, handler: Callable[[DomainEvent], Awaitable[None]]
    ) -> None:
        """
        Unsubscribe a handler from an event type.

        Args:
            event_type: Type of event
            handler: Handler to remove
        """
        pass

    @abstractmethod
    async def publish_batch(self, events: list[DomainEvent]) -> None:
        """
        Publish multiple events atomically.

        Args:
            events: List of events to publish
        """
        pass


class InMemoryEventBus(EventBus):
    """
    Simple in-memory event bus for testing and single-process deployments.
    NOT suitable for distributed systems - use RabbitMQ adapter for production.
    """

    def __init__(self):
        self._subscribers: dict[str, list[Callable]] = {}

    async def publish(self, event: DomainEvent) -> None:
        """Publish event to in-memory subscribers."""
        handlers = self._subscribers.get(event.event_type, [])
        for handler in handlers:
            await handler(event)

    async def subscribe(
        self, event_type: str, handler: Callable[[DomainEvent], Awaitable[None]]
    ) -> None:
        """Subscribe to event type."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)

    async def unsubscribe(
        self, event_type: str, handler: Callable[[DomainEvent], Awaitable[None]]
    ) -> None:
        """Unsubscribe from event type."""
        if event_type in self._subscribers:
            self._subscribers[event_type].remove(handler)

    async def publish_batch(self, events: list[DomainEvent]) -> None:
        """Publish multiple events."""
        for event in events:
            await self.publish(event)
