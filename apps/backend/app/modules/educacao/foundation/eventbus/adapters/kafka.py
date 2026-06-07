from __future__ import annotations

import json
import os
from typing import Any

try:
    from confluent_kafka import Producer
except Exception:  # pragma: no cover - optional dependency
    Producer = None


class KafkaEventBus:
    """Minimal Kafka adapter using confluent_kafka.Producer.

    Environment variables:
      - KAFKA_BOOTSTRAP (bootstrap servers, default localhost:9092)
    """

    def __init__(self, bootstrap: str | None = None) -> None:
        self.bootstrap = bootstrap or os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")
        self._producer = None

    def _ensure(self) -> None:
        if Producer is None:
            raise RuntimeError("confluent_kafka is required for KafkaEventBus but is not installed")
        if self._producer is None:
            self._producer = Producer({"bootstrap.servers": self.bootstrap})

    def publish(self, topic: str, event: dict[str, Any]) -> None:
        self._ensure()
        payload = json.dumps(event, default=str).encode("utf-8")
        self._producer.produce(topic, value=payload)
        # poll to serve delivery callbacks; non-blocking
        self._producer.poll(0)

    def flush(self, timeout: int = 5) -> None:
        if self._producer:
            self._producer.flush(timeout)
