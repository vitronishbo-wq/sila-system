from __future__ import annotations
import asyncio
import time
from datetime import datetime, timezone
from typing import Awaitable, Callable

class RankingWorker:

    def __init__(self, *, recalculate_fn: Callable[[], Awaitable[int] | int], interval_seconds: float=300.0) -> None:
        self.recalculate_fn = recalculate_fn
        self.interval_seconds = interval_seconds
        self.running = False
        self.stats: dict[str, int | float | str | None] = {'runs': 0, 'errors': 0, 'updated_items': 0, 'last_run_at': None, 'last_duration_ms': None}

    async def process_once(self) -> int:
        started = time.perf_counter()
        try:
            result = self.recalculate_fn()
            updated = await result if asyncio.iscoroutine(result) else result
            updated = int(updated or 0)
            self.stats['runs'] = int(self.stats['runs']) + 1
            self.stats['updated_items'] = int(self.stats['updated_items']) + updated
            return updated
        except Exception:
            self.stats['errors'] = int(self.stats['errors']) + 1
            raise
        finally:
            elapsed_ms = (time.perf_counter() - started) * 1000
            self.stats['last_duration_ms'] = round(elapsed_ms, 3)
            self.stats['last_run_at'] = datetime.now(timezone.utc).isoformat()

    async def run_forever(self) -> None:
        self.running = True
        while self.running:
            try:
                await self.process_once()
            except Exception:
                pass
            await asyncio.sleep(self.interval_seconds)

    def stop(self) -> None:
        self.running = False