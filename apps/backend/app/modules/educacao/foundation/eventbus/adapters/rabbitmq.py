from __future__ import annotations

import json
import os
from typing import Any

try:
    import pika
except Exception:  # pragma: no cover - optional dependency
    pika = None


class RabbitMQEventBus:
    """Minimal RabbitMQ event bus adapter using pika BlockingConnection.

    Environment variables:
      - RABBITMQ_URL (amqp url)
      - RABBITMQ_EXCHANGE (optional exchange name)
    """

    def __init__(self, url: str | None = None, exchange: str | None = None) -> None:
        self.url = url or os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/%2f")
        self.exchange = exchange or os.getenv("RABBITMQ_EXCHANGE", "")
        self._conn = None
        self._channel = None

    def _ensure(self) -> None:
        if pika is None:
            raise RuntimeError("pika is required for RabbitMQEventBus but is not installed")
        if self._conn is None:
            params = pika.URLParameters(self.url)
            self._conn = pika.BlockingConnection(params)
            self._channel = self._conn.channel()

    def publish(self, topic: str, event: dict[str, Any]) -> None:
        self._ensure()
        body = json.dumps(event, default=str).encode("utf-8")
        props = pika.BasicProperties(content_type="application/json")
        self._channel.basic_publish(exchange=self.exchange or "", routing_key=topic, body=body, properties=props)

    def close(self) -> None:
        if self._conn:
            try:
                self._conn.close()
            finally:
                self._conn = None
                self._channel = None
