from __future__ import annotations

import json
import os
from typing import Any


class Outbox:
    """Minimal outbox implementation: buffers events and flushes to an EventBusPort.

    In production this should be implemented with a DB-backed outbox table
    and a background dispatcher to guarantee at-least-once delivery.
    """

    def __init__(self, path: str | None = None) -> None:
        self.path = path or "data/foundation_outbox.jsonl"
        # ensure directory
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        self._buffer: list[dict[str, Any]] = []

    def enqueue(self, topic: str, event: dict[str, Any]) -> None:
        record = {"topic": topic, "event": event}
        self._buffer.append(record)
        # append to file for durability
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, default=str) + "\n")

    def flush(self, bus) -> None:
        # bus: object implementing publish(topic, event)
        for rec in list(self._buffer):
            try:
                bus.publish(rec["topic"], rec["event"])
                self._buffer.remove(rec)
            except Exception:
                # keep in buffer for retry
                continue
