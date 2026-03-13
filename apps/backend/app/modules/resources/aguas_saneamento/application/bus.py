from __future__ import annotations
from collections import defaultdict
from collections.abc import Awaitable, Callable
from typing import Any
EventHandler = Callable[[Any], Awaitable[None]]

class EventBus:

    def __init__(self) -> None:
        self._subscribers: dict[str, list[EventHandler]] = defaultdict(list)

    def subscribe(self, event_name: str, handler: EventHandler) -> None:
        handlers = self._subscribers[event_name]
        if handler not in handlers:
            handlers.append(handler)

    async def publish(self, event: Any) -> None:
        event_name = getattr(event, 'event_name', '')
        handlers = list(self._subscribers.get(event_name, []))
        for handler in handlers:
            await handler(event)
event_bus = EventBus()