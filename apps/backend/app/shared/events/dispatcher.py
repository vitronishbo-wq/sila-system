from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable

from .domain_event import DomainEvent

EventHandler = Callable[[DomainEvent], None]


class DomainEventDispatcher:
    """Simple in-memory dispatcher for module decoupling."""

    def __init__(self) -> None:
        self._handlers: dict[str, list[EventHandler]] = defaultdict(list)

    def register(self, event_type: str, handler: EventHandler) -> None:
        self._handlers[event_type].append(handler)

    def dispatch(self, event: DomainEvent) -> None:
        for handler in self._handlers.get(event.event_type, []):
            handler(event)
