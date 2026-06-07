"""Handler registry for event-to-handler mapping."""

from collections import defaultdict
from typing import Any

from apps.backend.app.core.observability.enterprise_logging import get_logger

logger = get_logger("core.events.registry")


class HandlerRegistry:
    """Global registry mapping event types to their handlers.

    Thread-safe registry using a class-level dictionary.
    Handlers are stored by event name and executed in registration order.

    Pattern: Supports runtime registration (tests, dynamic loading).

    Example:
        ```python
        # Register handlers
        HandlerRegistry.register("USER_LOGGED_IN", handler_instance)

        # Retrieve handlers
        handlers = HandlerRegistry.get("USER_LOGGED_IN")
        for handler in handlers:
            await handler.handle(event)
        ```
    """

    _handlers: dict[str, list] = defaultdict(list)

    @classmethod
    def register(cls, event_name: str, handler) -> None:
        """Register a handler for an event type.

        Args:
            event_name: Event type identifier (e.g., "USER_LOGGED_IN")
            handler: Handler instance (must implement EventHandler.handle)

        Raises:
            ValueError: If handler doesn't implement async handle method
        """
        if not hasattr(handler, "handle"):
            if not callable(handler):
                raise ValueError(f"Handler {handler} must implement handle method")
            fn = handler

            class _FunctionHandler:
                __name__ = getattr(fn, "__name__", "function_handler")

                async def handle(self, event: Any) -> None:
                    result = fn(event)
                    if hasattr(result, "__await__"):
                        await result

            handler = _FunctionHandler()
        cls._handlers[event_name].append(handler)
        logger.info(
            "handler_registered",
            extra={
                "event": event_name,
                "handler": handler.__class__.__name__,
                "total_handlers": len(cls._handlers[event_name]),
            },
        )

    @classmethod
    def get(cls, event_name: str) -> list:
        """Get all handlers for an event type.

        Args:
            event_name: Event type identifier

        Returns:
            List of handler instances for this event type (empty list if none)
        """
        handlers = cls._handlers.get(event_name, [])
        if not handlers:
            logger.debug("no_handlers_for_event", extra={"event": event_name})
        return handlers

    @classmethod
    def get_all(cls) -> dict:
        """Get mapping of all registered handlers."""
        return dict(cls._handlers)

    @classmethod
    def clear(cls) -> None:
        """Clear all registered handlers (useful for testing)."""
        cls._handlers.clear()
        logger.debug("all_handlers_cleared")

    @classmethod
    def get_stats(cls) -> dict:
        """Get registry statistics.

        Returns:
            dict: Statistics about registered handlers
        """
        return {
            "event_types": len(cls._handlers),
            "total_handlers": sum(len(h) for h in cls._handlers.values()),
            "by_event": {k: len(v) for k, v in cls._handlers.items()},
        }
