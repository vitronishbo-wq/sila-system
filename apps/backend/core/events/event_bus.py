"""Unified Event Bus - Single source of truth for pub/sub events."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Callable, Optional, List
import asyncio
from datetime import datetime


class Event:
    """Base event class."""
    
    def __init__(self, event_type: str, payload: Dict[str, Any]):
        self.event_type = event_type
        self.payload = payload
        self.timestamp = datetime.utcnow()
        self.id = id(self)
    
    def __repr__(self):
        return f"Event(type={self.event_type}, timestamp={self.timestamp})"


class EventBusPort(ABC):
    """Abstract event bus interface.
    
    Consolidates 2 duplicate implementations:
    - app/modules/service_requests/application/ports/event_bus_port.py
    - modules/taxpayer/application/ports/event_bus_port.py
    """

    @abstractmethod
    async def publish(self, event_type: str, payload: Dict[str, Any]) -> None:
        """Publish event to bus.
        
        Args:
            event_type: Type of event (e.g., 'user.created', 'payment.completed')
            payload: Event data
        """
        pass

    @abstractmethod
    async def subscribe(self, event_type: str, handler: Callable) -> None:
        """Subscribe to event type.
        
        Args:
            event_type: Type of event to subscribe to
            handler: Async callback handler
        """
        pass

    @abstractmethod
    async def unsubscribe(self, event_type: str, handler: Callable) -> None:
        """Unsubscribe from event.
        
        Args:
            event_type: Type of event
            handler: Handler to remove
        """
        pass


class InMemoryEventBus(EventBusPort):
    """In-memory implementation of EventBus for development/testing."""

    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}

    async def publish(self, event_type: str, payload: Dict[str, Any]) -> None:
        """Publish event to all subscribers."""
        event = Event(event_type, payload)
        handlers = self._subscribers.get(event_type, [])
        
        tasks = [handler(event) for handler in handlers]
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def subscribe(self, event_type: str, handler: Callable) -> None:
        """Subscribe handler to event type."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)

    async def unsubscribe(self, event_type: str, handler: Callable) -> None:
        """Unsubscribe handler from event type."""
        if event_type in self._subscribers:
            self._subscribers[event_type] = [
                h for h in self._subscribers[event_type] if h != handler
            ]


# Singleton instance
_event_bus: Optional[InMemoryEventBus] = None


def get_event_bus() -> EventBusPort:
    """Get or create event bus singleton."""
    global _event_bus
    if _event_bus is None:
        _event_bus = InMemoryEventBus()
    return _event_bus

