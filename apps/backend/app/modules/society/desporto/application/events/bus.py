from __future__ import annotations
import asyncio
from collections import defaultdict
from typing import Awaitable, Callable
EventHandler = Callable[[object], Awaitable[None] | None]

class EventBus:

    def __init__(self) -> None:
        self._handlers: dict[str, list[EventHandler]] = defaultdict(list)

    def subscribe(self, event_name: str, handler: EventHandler) -> None:
        self._handlers[event_name].append(handler)

    async def publish(self, event: object) -> None:
        handlers = list(self._handlers.get(type(event).__name__, []))
        for handler in handlers:
            result = handler(event)
            if asyncio.iscoroutine(result):
                await result
event_bus = EventBus()