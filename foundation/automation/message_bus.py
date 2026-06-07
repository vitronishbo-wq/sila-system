from __future__ import annotations

import logging
import os
import threading
from collections.abc import Callable
from typing import Any

from kombu import Connection, Exchange, Producer, Queue
from kombu.mixins import ConsumerMixin

logger = logging.getLogger(__name__)

AutomationHandler = Callable[[dict[str, Any]], None]


class LocalAutomationBus:
    """In-memory automation bus used when no broker is configured."""

    def __init__(self) -> None:
        self._subscribers: dict[str, list[AutomationHandler]] = {}

    def publish(self, topic: str, event: dict[str, Any]) -> None:
        handlers = self._subscribers.get(topic, [])
        logger.debug("LocalAutomationBus.publish topic=%s handlers=%d", topic, len(handlers))
        for handler in handlers:
            try:
                handler(event)
            except Exception:
                logger.exception("LocalAutomationBus handler failed for %s", topic)

    def subscribe(self, topic: str, handler: AutomationHandler) -> None:
        self._subscribers.setdefault(topic, []).append(handler)
        logger.debug("LocalAutomationBus.subscribe topic=%s handler=%s", topic, handler)

    def start(self) -> None:
        return None

    def stop(self) -> None:
        return None


class _RabbitMQConsumer(ConsumerMixin):
    def __init__(self, broker_url: str, queues: list[Queue], on_message: AutomationHandler) -> None:
        self.connection = Connection(broker_url)
        self.queues = queues
        self.on_message = on_message

    def get_consumers(self, Consumer, channel):
        return [Consumer(queue=q, callbacks=[self._wrapped_callback], accept=["json"]) for q in self.queues]

    def _wrapped_callback(self, body: dict[str, Any], message) -> None:
        try:
            self.on_message(body)
            message.ack()
        except Exception:
            logger.exception("RabbitMQ automation consumer failed")
            message.reject()

    def on_connection_error(self, exc, interval):
        logger.warning("RabbitMQ consumer connection error: %s, retrying in %s seconds", exc, interval)


class RabbitMQAutomationBus:
    """RabbitMQ automation bus using Kombu and topic exchange with DLX support."""

    DEFAULT_EXCHANGE = "sila.automation"
    DEFAULT_DLX_EXCHANGE = "sila.automation.dlx"
    DEFAULT_DLQ_QUEUE = "sila_dlq_main"

    def __init__(
        self,
        broker_url: str | None = None,
        exchange_name: str | None = None,
        dlx_enabled: bool = True,
        max_retries: int = 3,
    ) -> None:
        self.broker_url = broker_url or os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672//")
        self.exchange_name = exchange_name or os.getenv("RABBITMQ_EXCHANGE", self.DEFAULT_EXCHANGE)
        self.dlx_exchange_name = os.getenv("RABBITMQ_DLX_EXCHANGE", self.DEFAULT_DLX_EXCHANGE)
        self.dlq_queue_name = os.getenv("RABBITMQ_DLQ_QUEUE", self.DEFAULT_DLQ_QUEUE)
        self.dlx_enabled = dlx_enabled and os.getenv("DLQ_ENABLED", "true").lower() in ("true", "1", "yes")
        self.max_retries = int(os.getenv("DLQ_MAX_RETRIES", str(max_retries)))

        self.exchange = Exchange(self.exchange_name, type="topic", durable=True)
        self.dlx_exchange = Exchange(self.dlx_exchange_name, type="topic", durable=True) if self.dlx_enabled else None

        self._subscribers: dict[str, list[AutomationHandler]] = {}
        self._queues: dict[str, Queue] = {}
        self._consumer: _RabbitMQConsumer | None = None
        self._thread: threading.Thread | None = None
        self._dlx_setup_done = False

        logger.info(
            "RabbitMQAutomationBus initialized with DLX=%s max_retries=%d",
            self.dlx_enabled,
            self.max_retries,
        )

    def _setup_dlx_for_queue(self, queue: Queue) -> Queue:
        """Configure DLX arguments for a queue."""
        if not self.dlx_enabled or not self.dlx_exchange:
            return queue

        # Extract routing key from queue definition
        routing_key = queue.routing_key or queue.name
        dlx_routing_key = f"dlq.{routing_key}"

        # Add DLX arguments to queue
        queue.queue_arguments = queue.queue_arguments or {}
        queue.queue_arguments.update({
            "x-dead-letter-exchange": self.dlx_exchange_name,
            "x-dead-letter-routing-key": dlx_routing_key,
        })

        logger.debug(
            "DLX configured for queue=%s routing_key=%s dlx_routing_key=%s",
            queue.name,
            routing_key,
            dlx_routing_key,
        )
        return queue

    def _ensure_dlx_setup(self) -> None:
        """Ensure DLX and DLQ are created in RabbitMQ."""
        if not self.dlx_enabled or self._dlx_setup_done:
            return

        try:
            with Connection(self.broker_url) as conn:
                # Create DLX exchange
                self.dlx_exchange(conn.default_channel).declare()

                # Create DLQ queue bound to all DLX messages
                dlq_queue = Queue(
                    self.dlq_queue_name,
                    exchange=self.dlx_exchange,
                    routing_key="dlq.#",  # Match all dead letter routing keys
                    durable=True,
                    declare=True,
                )
                dlq_queue.declare(conn.default_channel)

                self._dlx_setup_done = True
                logger.info(
                    "DLX setup complete: exchange=%s queue=%s",
                    self.dlx_exchange_name,
                    self.dlq_queue_name,
                )
        except Exception as exc:
            logger.error("Failed to setup DLX: %s", exc)
            # Don't fail completely - system should work without DLX if RabbitMQ doesn't support it
            self._dlx_setup_done = True  # Mark as attempted to avoid retry storms

    def publish(self, topic: str, event: dict[str, Any]) -> None:
        logger.debug(
            "RabbitMQAutomationBus.publish exchange=%s topic=%s student_id=%s",
            self.exchange_name,
            topic,
            event.get("request", {}).get("student_id", "N/A"),
        )
        try:
            with Connection(self.broker_url) as conn:
                producer = Producer(conn)
                producer.publish(
                    event,
                    exchange=self.exchange,
                    routing_key=topic,
                    serializer="json",
                    declare=[self.exchange],
                    retry=True,
                    retry_policy={"max_retries": 3},
                )
        except Exception as exc:
            logger.error("Failed to publish to topic=%s: %s", topic, exc)
            raise

    def subscribe(self, topic: str, handler: AutomationHandler) -> None:
        self._subscribers.setdefault(topic, []).append(handler)
        queue_name = f"sila_{topic}"

        # Create queue with DLX support
        queue = Queue(
            queue_name,
            exchange=self.exchange,
            routing_key=topic,
            durable=True,
        )
        queue = self._setup_dlx_for_queue(queue)
        self._queues[topic] = queue

        logger.debug("RabbitMQAutomationBus.subscribe topic=%s queue=%s dlx_enabled=%s", topic, queue_name, self.dlx_enabled)

        if self._thread and self._thread.is_alive():
            self.stop()
            self.start()

    def _handle_message(self, payload: dict[str, Any]) -> None:
        topic = payload.get("event_type") or payload.get("type")
        student_id = payload.get("request", {}).get("student_id", payload.get("student_id", "N/A"))

        if not topic:
            logger.warning("RabbitMQAutomationBus received message without event_type: %s", payload)
            return

        handlers = self._subscribers.get(topic, [])
        logger.debug(
            "RabbitMQAutomationBus handling topic=%s handlers=%d student_id=%s",
            topic,
            len(handlers),
            student_id,
        )
        for handler in handlers:
            try:
                handler(payload)
            except Exception:
                logger.exception("RabbitMQAutomationBus subscriber raised for topic=%s student_id=%s", topic, student_id)

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        if not self._queues:
            return

        # Ensure DLX/DLQ are setup before starting consumer
        self._ensure_dlx_setup()

        self._consumer = _RabbitMQConsumer(self.broker_url, list(self._queues.values()), self._handle_message)
        self._thread = threading.Thread(target=self._consumer.run, daemon=True)
        self._thread.start()
        logger.info("RabbitMQAutomationBus consumer started for %d topics with DLX=%s", len(self._queues), self.dlx_enabled)

    def stop(self) -> None:
        if self._consumer:
            self._consumer.should_stop = True
        if self._thread:
            self._thread.join(timeout=2.0)
        self._consumer = None
        self._thread = None
        logger.info("RabbitMQAutomationBus stopped")


def build_automation_bus(bus_type: str | None = None):
    # If explicit bus_type provided use it; otherwise prefer configured broker
    env_selection = os.getenv("AUTOMATION_BUS")
    selection = (bus_type or env_selection or "").lower()
    # Auto-detect RabbitMQ when RABBITMQ_URL is present and no explicit selection
    if not selection:
        if os.getenv("RABBITMQ_URL"):
            selection = "rabbit"
        else:
            selection = os.getenv("AUTOMATION_BUS", "local").lower() or "local"

    if selection in ("rabbit", "rabbitmq"):
        try:
            return RabbitMQAutomationBus()
        except Exception as exc:
            logger.warning("RabbitMQ automation bus unavailable, falling back to local bus: %s", exc)
            return LocalAutomationBus()
    if selection in ("local", "inmemory", "memory"):
        return LocalAutomationBus()
    raise ValueError(f"Unsupported automation bus type: {selection}")
