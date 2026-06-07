from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable


class EstatisticaWorker:
    def __init__(
        self, *, collect_fn: Callable[[], Awaitable[int] | int], interval_seconds: float = 120.0
    ) -> None:
        self.collect_fn = collect_fn
        self.interval_seconds = interval_seconds
        self.running = False
        self.stats: dict[str, int] = {"runs": 0, "errors": 0, "processed_items": 0}

    async def process_once(self) -> int:
        result = self.collect_fn()
        processed = await result if asyncio.iscoroutine(result) else result
        processed = int(processed or 0)
        self.stats["runs"] += 1
        self.stats["processed_items"] += processed
        return processed

    async def run_forever(self) -> None:
        self.running = True
        while self.running:
            try:
                await self.process_once()
            except Exception:
                self.stats["errors"] += 1
            await asyncio.sleep(self.interval_seconds)

    def stop(self) -> None:
        self.running = False
