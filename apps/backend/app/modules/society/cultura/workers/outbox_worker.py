from __future__ import annotations

import asyncio
from collections.abc import Callable
from datetime import datetime


class OutboxWorker:
    def __init__(
        self,
        *,
        outbox,
        event_publisher: Callable[[dict], object] | None = None,
        interval_seconds: int = 10,
        batch_size: int = 100,
    ) -> None:
        self.outbox = outbox
        self.event_publisher = event_publisher
        self.interval_seconds = interval_seconds
        self.batch_size = batch_size
        self.running = False
        self.stats = {"publicados": 0, "falhas": 0, "ultimo_lote": None}

    async def start(self) -> None:
        self.running = True
        while self.running:
            await self._processar_lote()
            await asyncio.sleep(self.interval_seconds)

    async def stop(self) -> None:
        self.running = False

    async def _processar_lote(self) -> None:
        events = await self.outbox.pop_batch(self.batch_size)
        if not events:
            return
        for event in events:
            try:
                if self.event_publisher is not None:
                    result = self.event_publisher(event)
                    if asyncio.iscoroutine(result):
                        await result
                self.stats["publicados"] += 1
            except Exception:
                self.stats["falhas"] += 1
        self.stats["ultimo_lote"] = datetime.utcnow().isoformat()
