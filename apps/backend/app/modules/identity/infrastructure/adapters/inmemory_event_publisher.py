from typing import Any, Callable, Dict, List
from apps.backend.app.modules.identity.domain.ports.event_publisher_port import EventPublisherPort

class InMemoryEventPublisher(EventPublisherPort):
    """Adapter: In-memory event publisher for testing and development."""

    def __init__(self):
        self.handlers: Dict[str, List[Callable]] = {}

    async def publish(self, event_name: str, event_data: Dict[str, Any]) -> None:
        """Publish an event to all subscribers."""
        if event_name in self.handlers:
            for handler in self.handlers[event_name]:
                await handler(event_data)

    async def subscribe(self, event_name: str, handler: Callable) -> None:
        """Subscribe to an event."""
        if event_name not in self.handlers:
            self.handlers[event_name] = []
        self.handlers[event_name].append(handler)

    async def unsubscribe(self, event_name: str, handler: Callable) -> None:
        """Unsubscribe from an event."""
        if event_name in self.handlers:
            if handler in self.handlers[event_name]:
                self.handlers[event_name].remove(handler)