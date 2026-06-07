"""Enhanced event bus with Redis broker integration."""

import asyncio
from typing import Any

from apps.backend.app.core.observability.enterprise_logging import get_logger

from .broker import RedisBroker
from .models import DomainEvent
from .registry import HandlerRegistry

logger = get_logger("core.events.bus")


class EventBus:
    """Global event bus for publishing and dispatching domain events.

    Responsibilities:
    1. Publishing events to Redis pub/sub for cross-service notifications
    2. Dispatching events to local handlers via registry
    3. Maintaining event correlation for observability
    4. Error handling and logging

    Pattern: Static methods for convenient access (singleton pattern)

    Example:
        ```python
        # Publish event (goes to Redis + local handlers)
        event = UserLoggedIn(user_id="123", request_id="req_456")
        await EventBus.publish(event)

        # Subscribe handler
        class MyHandler(EventHandler):
            async def handle(self, event):
                print(f"Received: {event.name}")

        HandlerRegistry.register("USER_LOGGED_IN", MyHandler())
        ```
    """

    _broker: RedisBroker = None
    _initialized: bool = False

    @classmethod
    def initialize(cls, broker: RedisBroker = None) -> None:
        """Initialize the event bus with optional custom broker.

        Args:
            broker: Custom broker instance (defaults to RedisBroker)
        """
        if not cls._initialized:
            cls._broker = broker or RedisBroker()
            cls._initialized = True
            logger.info("event_bus_initialized")

    @classmethod
    async def publish(cls, event: DomainEvent) -> None:
        """Publish event to both Redis and local handlers.

        Args:
            event: Domain event to publish

        Raises:
            RuntimeError: If bus not initialized
        """
        if not cls._initialized:
            cls.initialize()
        logger.info(
            "event_published",
            extra={
                "event_name": event.name,
                "event_id": event.id,
                "request_id": event.metadata.get("request_id", "N/A"),
            },
        )
        try:
            message_dict = {
                "name": event.name,
                "payload": event.payload,
                "id": event.id,
                "occurred_at": event.occurred_at.isoformat(),
                "version": event.version,
                "metadata": event.metadata,
            }
            await cls._broker.publish(channel=event.name, message=message_dict)
            await cls.dispatch(event)
        except Exception as e:
            logger.error("event_bus_publish_failed", extra={"event": event.name, "error": str(e)})
            raise

    @classmethod
    async def dispatch(cls, event: DomainEvent) -> None:
        """Dispatch event to all registered local handlers.

        Handlers are executed sequentially. Exceptions in handlers are logged
        but don't prevent other handlers from executing.

        Args:
            event: Domain event to dispatch
        """
        handlers = HandlerRegistry.get(event.name)
        if not handlers:
            logger.debug("no_handlers_for_event", extra={"event": event.name})
            return
        for handler in handlers:
            try:
                if asyncio.iscoroutinefunction(handler.handle):
                    await handler.handle(event)
                else:
                    handler.handle(event)
                logger.debug(
                    "handler_executed_successfully",
                    extra={"event": event.name, "handler": handler.__class__.__name__},
                )
            except Exception as exc:
                logger.error(
                    "handler_execution_failed",
                    extra={
                        "event": event.name,
                        "handler": handler.__class__.__name__,
                        "error": str(exc),
                    },
                )

    @classmethod
    async def health_check(cls) -> dict[str, Any]:
        """Check health of event bus infrastructure.

        Returns:
            dict: Health status including broker state and handler registry
        """
        if not cls._initialized:
            cls.initialize()
        broker_healthy = await cls._broker.health_check()
        registry_stats = HandlerRegistry.get_stats()
        return {
            "status": "healthy" if broker_healthy else "degraded",
            "broker": {"name": "Redis", "healthy": broker_healthy},
            "registry": registry_stats,
        }
