from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Optional


class EventPriority(str, Enum):
    HIGH = "high"
    NORMAL = "normal"
    LOW = "low"


@dataclass
class Event:
    id: str
    name: str
    source_module: str
    payload: dict[str, Any]
    priority: EventPriority = EventPriority.NORMAL
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    correlation_id: Optional[str] = None


@dataclass
class Subscription:
    module: str
    event_name: str
    handler: Optional[Callable] = None


class EventBus:
    """Barramento de eventos para comunicação assíncrona entre módulos.
    
    Permite que módulos publiquem eventos (ex.: citizen_updated, student_enrolled)
    sem conhecerem quem consome — desacoplamento total.
    """

    def __init__(self) -> None:
        self._subscriptions: dict[str, list[Subscription]] = {}
        self._history: list[Event] = []

    def subscribe(self, module: str, event_name: str) -> Subscription:
        sub = Subscription(module=module, event_name=event_name)
        self._subscriptions.setdefault(event_name, []).append(sub)
        return sub

    def publish(self, event: Event) -> list[Subscription]:
        self._history.append(event)
        matched = self._subscriptions.get(event.name, [])
        for sub in matched:
            if sub.handler:
                try:
                    sub.handler(event)
                except Exception:
                    pass
        return matched

    def get_subscribers(self, event_name: str) -> list[Subscription]:
        return self._subscriptions.get(event_name, [])

    def get_history(self, module: Optional[str] = None,
                    event_name: Optional[str] = None,
                    limit: int = 100) -> list[Event]:
        results = self._history
        if module:
            results = [e for e in results if e.source_module == module]
        if event_name:
            results = [e for e in results if e.name == event_name]
        return results[-limit:]

    def count_by_event(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for e in self._history:
            counts[e.name] = counts.get(e.name, 0) + 1
        return counts
