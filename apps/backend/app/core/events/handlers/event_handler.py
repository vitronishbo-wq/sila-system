"""Base event handler interface and implementations."""
from abc import ABC, abstractmethod
from typing import Any

class EventHandler(ABC):
    """Abstract base class for all event handlers.
    
    Event handlers are components that react to published events.
    Each handler is registered to specific event types via HandlerRegistry.
    
    Handlers should be idempotent (safe to call multiple times with same input).
    
    Example:
        ```python
        class NotifyHealthServiceHandler(EventHandler):
            async def handle(self, event):
                if event.name == "USER_LOGGED_IN":
                    await notify_health_service(event.payload['user_id'])
        
        registry = HandlerRegistry()
        registry.register("USER_LOGGED_IN", NotifyHealthServiceHandler())
        ```
    """

    @property
    def event_type(self) -> str:
        """Event type this handler processes."""
        return '*'

    @abstractmethod
    async def handle(self, event: Any) -> None:
        """Handle a domain event.
        
        Args:
            event: Domain event instance with name, payload, metadata
            
        Raises:
            Exception: Should propagate exceptions for proper error handling
        """
        pass