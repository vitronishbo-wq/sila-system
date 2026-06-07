from __future__ import annotations

from dataclasses import asdict, is_dataclass
from datetime import datetime
from typing import Any


class InMemoryOutbox:
    def __init__(self) -> None:
        self._events: list[dict[str, Any]] = []

    async def append(self, event: object) -> None:
        if hasattr(event, "to_payload") and callable(event.to_payload):
            payload = dict(event.to_payload())
        elif is_dataclass(event):
            payload = asdict(event)
        else:
            payload = {"repr": repr(event)}
        self._events.append(
            {
                "event_name": type(event).__name__,
                "payload": payload,
                "created_at": datetime.utcnow().isoformat(),
            }
        )

    async def list_events(self) -> list[dict[str, Any]]:
        return list(self._events)

    async def pop_batch(self, batch_size: int = 100) -> list[dict[str, Any]]:
        if batch_size <= 0:
            return []
        batch = self._events[:batch_size]
        self._events = self._events[batch_size:]
        return batch

    async def clear(self) -> None:
        self._events.clear()
