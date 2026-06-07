"""Event worker for consuming pub/sub messages from Redis.

This is a long-running process that subscribes to event channels
and dispatches them to registered handlers.

Run with:
    python app/workers/event_worker.py
"""

import asyncio
import json
import signal
import sys

from apps.backend.app.core.events.broker import RedisBroker
from apps.backend.app.core.events.models import DomainEvent
from apps.backend.app.core.events.registry import HandlerRegistry
from apps.backend.app.core.observability.context import set_request_context
from apps.backend.app.core.observability.enterprise_logging import (
    get_logger,
    setup_enterprise_logging,
)

logger = get_logger("workers.event_worker")
try:
    from apps.backend.app.modules.educacao.application.events import handlers as educacao_handlers
except ImportError:
    logger.warning("educacao_handlers not found")


class EventWorker:
    """Worker that consumes events and dispatches to handlers."""

    def __init__(self, broker: RedisBroker = None):
        self.broker = broker or RedisBroker()
        self.running = False
        self.subscriptions = {}

    async def subscribe_to_event(self, event_name: str) -> None:
        """Subscribe to a specific event type.

        Args:
            event_name: Event type to subscribe to
        """
        logger.info("subscribing_to_event_channel", extra={"event": event_name})
        try:
            async for message in self.broker.subscribe(event_name):
                await self._handle_message(event_name, message)
        except asyncio.CancelledError:
            logger.info("subscription_cancelled", extra={"event": event_name})
        except Exception as e:
            logger.error("subscription_error", extra={"event": event_name, "error": str(e)})

    async def _handle_message(self, channel: str, message: str) -> None:
        """Process a single event message.

        Args:
            channel: Channel the message came from
            message: JSON-encoded message
        """
        try:
            payload = json.loads(message)
            if "metadata" in payload and "request_id" in payload["metadata"]:
                set_request_context(request_id=payload["metadata"]["request_id"])
            logger.debug(
                "event_received",
                extra={"event": payload.get("name", "UNKNOWN"), "channel": channel},
            )
            event = DomainEvent(
                name=payload.get("name", ""),
                payload=payload.get("payload", {}),
                id=payload.get("id", ""),
                version=payload.get("version", "1.0"),
                metadata=payload.get("metadata", {}),
            )
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
                        "handler_executed",
                        extra={"event": event.name, "handler": handler.__class__.__name__},
                    )
                except Exception as exc:
                    logger.error(
                        "handler_failed",
                        extra={
                            "event": event.name,
                            "handler": handler.__class__.__name__,
                            "error": str(exc),
                        },
                    )
        except json.JSONDecodeError as e:
            logger.error("failed_to_parse_event", extra={"error": str(e), "message": message})
        except Exception as e:
            logger.error("event_processing_failed", extra={"error": str(e)})

    async def start(self) -> None:
        """Start the event worker and listen to all registered event types."""
        self.running = True
        logger.info("event_worker_starting")
        registry_stats = HandlerRegistry.get_stats()
        event_types = list(registry_stats.get("by_event", {}).keys())
        if not event_types:
            logger.warning("no_event_handlers_registered")
            return
        logger.info(
            "subscribing_to_events", extra={"event_count": len(event_types), "events": event_types}
        )
        tasks = [self.subscribe_to_event(event_type) for event_type in event_types]
        try:
            await asyncio.gather(*tasks)
        except KeyboardInterrupt:
            logger.info("keyboard_interrupt_received")
            await self.stop()
        except Exception as e:
            logger.error("worker_error", extra={"error": str(e)})
            await self.stop()

    async def stop(self) -> None:
        """Stop the event worker gracefully."""
        self.running = False
        logger.info("event_worker_stopping")


async def main():
    """Main entry point for event worker."""
    setup_enterprise_logging(service_name="event-worker", environment="production")
    logger.info("event_worker_initialized")
    worker = EventWorker()

    def signal_handler(signum, frame):
        logger.info("signal_received", extra={"signal": signum})
        asyncio.create_task(worker.stop())

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    await worker.start()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.error("worker_fatal_error", extra={"error": str(e)})
        sys.exit(1)
