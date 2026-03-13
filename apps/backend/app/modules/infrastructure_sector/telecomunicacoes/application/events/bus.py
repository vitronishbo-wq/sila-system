from __future__ import annotations
import asyncio
from collections import defaultdict
from collections.abc import Awaitable, Callable
from typing import Any
EventHandler = Callable[[Any], Awaitable[None]]

class EventBus:

    def __init__(self) -> None:
        self._handlers: dict[type, list[EventHandler]] = defaultdict(list)

    def subscribe(self, event_type: type, handler: EventHandler) -> None:
        handlers = self._handlers[event_type]
        if handler not in handlers:
            handlers.append(handler)

    async def publish(self, event: Any) -> None:
        handlers = list(self._handlers.get(type(event), []))
        if not handlers:
            return
        await asyncio.gather(*(handler(event) for handler in handlers))
event_bus = EventBus()