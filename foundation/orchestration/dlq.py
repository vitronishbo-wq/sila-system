from __future__ import annotations

import json
import logging
import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

try:
    from kombu import Connection, Exchange, Producer
except ImportError:  # pragma: no cover - optional dependency
    Connection = None
    Exchange = None
    Producer = None

logger = logging.getLogger(__name__)


class DeadLetterQueue(ABC):
    """Abstract dead letter queue sink."""

    @abstractmethod
    def record(self, entry: dict[str, Any]) -> None:
        pass


class FileDeadLetterQueue(DeadLetterQueue):
    """Fallback dead letter queue backed by a local file."""

    def __init__(self, path: str | None = None) -> None:
        self.path = Path(path or os.getenv("DLQ_PATH", "reports/orchestrator_dlq.log"))
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def record(self, entry: dict[str, Any]) -> None:
        try:
            with self.path.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except Exception as exc:
            logger.exception("Failed to write to file DLQ: %s", exc)


class RabbitMQDeadLetterQueue(DeadLetterQueue):
    """RabbitMQ-backed dead letter queue sink."""

    def __init__(
        self,
        broker_url: str | None = None,
        exchange_name: str | None = None,
        routing_key: str | None = None,
    ) -> None:
        self.broker_url = broker_url or os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672//")
        self.exchange_name = exchange_name or os.getenv("RABBITMQ_DLQ_EXCHANGE", "sila.automation.dlx")
        self.routing_key = routing_key or os.getenv("RABBITMQ_DLQ_ROUTING_KEY", "dead_letter")
        self._connection = None
        self._exchange = None

    def _ensure(self) -> None:
        if Connection is None or Exchange is None or Producer is None:
            raise RuntimeError("kombu is required for RabbitMQDeadLetterQueue but is not installed")
        if self._connection is None:
            self._connection = Connection(self.broker_url)
            self._connection.connect()
            self._exchange = Exchange(self.exchange_name, type="topic", durable=True)

    def record(self, entry: dict[str, Any]) -> None:
        try:
            self._ensure()
            producer = Producer(self._connection)
            producer.publish(
                entry,
                exchange=self._exchange,
                routing_key=self.routing_key,
                serializer="json",
                retry=True,
                retry_policy={"max_retries": 3, "interval_start": 0.2, "interval_step": 0.2, "interval_max": 1.0},
            )
        except Exception as exc:
            logger.exception("Failed to publish DLQ record to RabbitMQ: %s", exc)
            raise


def build_dead_letter_queue() -> DeadLetterQueue:
    """Build the configured dead letter queue sink.

    Supported backend options are:
    - file: simple local file sink
    - rabbitmq: publish failed records to RabbitMQ
    """
    selection = os.getenv("DLQ_BUS", "file").lower()
    if selection in ("rabbit", "rabbitmq"):
        try:
            return RabbitMQDeadLetterQueue()
        except Exception as exc:
            logger.warning("RabbitMQ DLQ unavailable, falling back to file DLQ: %s", exc)
    return FileDeadLetterQueue()
