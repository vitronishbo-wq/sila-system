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
        event_name = type(event).__name__
        handlers = list(self._handlers.get(event_name, []))
        for handler in handlers:
            result = handler(event)
            if asyncio.iscoroutine(result):
                await result
event_bus = EventBus()