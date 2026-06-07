"""
RabbitMQ Event Bus Adapter
Implements event publishing via message broker for distributed systems.
"""

import json
import logging
from collections.abc import Awaitable, Callable

try:
    import aio_pika
    from aio_pika import Channel, Exchange, connect_robust
except ImportError:
    raise ImportError("aio_pika not installed. Install with: pip install aio-pika") from None
from apps.backend.app.core.events.domain_event import DomainEvent
from apps.backend.app.core.events.event_bus import EventBus

logger = logging.getLogger(__name__)


class RabbitMQEventBus(EventBus):
    """
    Event Bus implementation using RabbitMQ.

    Configuration:
        RABBITMQ_URL: Connection string (default: amqp://guest:guest@localhost/)
        RABBITMQ_EXCHANGE: Exchange name (default: domain_events)
        RABBITMQ_QUEUE_PREFIX: Queue prefix (default: sila_)
    """

    def __init__(
        self,
        rabbitmq_url: str = "amqp://guest:guest@localhost/",
        exchange_name: str = "domain_events",
        queue_prefix: str = "sila_",
    ):
        self.rabbitmq_url = rabbitmq_url
        self.exchange_name = exchange_name
        self.queue_prefix = queue_prefix
        self._connection: aio_pika.Connection | None = None
        self._channel: Channel | None = None
        self._exchange: Exchange | None = None
        self._subscribers: dict[str, list[Callable]] = {}

    async def connect(self) -> None:
        """Establish RabbitMQ connection."""
        try:
            self._connection = await connect_robust(self.rabbitmq_url)
            self._channel = await self._connection.channel()
            self._exchange = await self._channel.declare_exchange(
                self.exchange_name, aio_pika.ExchangeType.TOPIC, durable=True
            )
            logger.info(f"Connected to RabbitMQ at {self.rabbitmq_url}")
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            raise

    async def disconnect(self) -> None:
        """Close RabbitMQ connection."""
        if self._connection:
            await self._connection.close()
            self._connection = None
            self._channel = None
            self._exchange = None

    async def publish(self, event: DomainEvent) -> None:
        """Publish a single event to RabbitMQ."""
        if not self._exchange:
            raise RuntimeError("RabbitMQ not connected. Call connect() first.")
        try:
            message = aio_pika.Message(
                body=json.dumps(event.to_dict()).encode(),
                content_type="application/json",
                headers={
                    "event_type": event.event_type,
                    "aggregate_type": event.aggregate_type,
                    "aggregate_id": str(event.aggregate_id),
                },
            )
            routing_key = f"{event.aggregate_type.lower()}.{event.event_type.lower()}"
            await self._exchange.publish(message, routing_key=routing_key)
            logger.debug(f"Published event {event.event_type} to {routing_key}")
        except Exception as e:
            logger.error(f"Failed to publish event {event.event_type}: {e}")
            raise

    async def publish_batch(self, events: list[DomainEvent]) -> None:
        """Publish multiple events (batch operation)."""
        for event in events:
            await self.publish(event)

    async def subscribe(
        self, event_type: str, handler: Callable[[DomainEvent], Awaitable[None]]
    ) -> None:
        """
        Subscribe to an event type.

        Args:
            event_type: Type of event (e.g., "CitizenCreated")
            handler: Async callback to handle events
        """
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)
        if len(self._subscribers[event_type]) == 1:
            await self._setup_consumer(event_type)

    async def unsubscribe(
        self, event_type: str, handler: Callable[[DomainEvent], Awaitable[None]]
    ) -> None:
        """Unsubscribe a handler from an event type."""
        if event_type in self._subscribers:
            self._subscribers[event_type].remove(handler)

    async def _setup_consumer(self, event_type: str) -> None:
        """Set up RabbitMQ consumer for an event type."""
        if not self._exchange:
            raise RuntimeError("RabbitMQ not connected.")
        try:
            queue_name = f"{self.queue_prefix}{event_type.lower()}"
            queue = await self._channel.declare_queue(queue_name, durable=True)
            routing_key = f"*.{event_type.lower()}"
            await queue.bind(self._exchange, routing_key=routing_key)
            await queue.consume(lambda msg: self._handle_message(event_type, msg), no_ack=False)
            logger.info(f"Setup consumer for event type: {event_type}")
        except Exception as e:
            logger.error(f"Failed to setup consumer for {event_type}: {e}")
            raise

    async def _handle_message(self, event_type: str, message: aio_pika.IncomingMessage) -> None:
        """Handle incoming message from RabbitMQ."""
        try:
            async with message.process():
                event_data = json.loads(message.body.decode())
                event = DomainEvent.from_dict(event_data)
                handlers = self._subscribers.get(event_type, [])
                for handler in handlers:
                    try:
                        await handler(event)
                    except Exception as e:
                        logger.error(f"Handler error for {event_type}: {e}")
        except Exception as e:
            logger.error(f"Error processing message: {e}")
