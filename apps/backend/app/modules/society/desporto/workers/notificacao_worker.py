from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable


class NotificacaoWorker:
    def __init__(
        self,
        *,
        dispatch_fn: Callable[[object], Awaitable[None] | None],
        source_fn: Callable[[int], Awaitable[list[object]] | list[object]],
        interval_seconds: float = 10.0,
        batch_size: int = 100,
    ) -> None:
        self.dispatch_fn = dispatch_fn
        self.source_fn = source_fn
        self.interval_seconds = interval_seconds
        self.batch_size = batch_size
        self.running = False
        self.stats: dict[str, int] = {"sent": 0, "errors": 0}

    async def process_once(self) -> int:
        source_result = self.source_fn(self.batch_size)
        items = await source_result if asyncio.iscoroutine(source_result) else source_result
        sent = 0
        for item in items:
            try:
                result = self.dispatch_fn(item)
                if asyncio.iscoroutine(result):
                    await result
                sent += 1
                self.stats["sent"] += 1
            except Exception:
                self.stats["errors"] += 1
        return sent

    async def run_forever(self) -> None:
        self.running = True
        while self.running:
            await self.process_once()
            await asyncio.sleep(self.interval_seconds)

    def stop(self) -> None:
        self.running = False
