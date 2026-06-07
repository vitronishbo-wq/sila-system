from __future__ import annotations

import asyncio
import logging
from datetime import datetime


class OutboxWorker:
    def __init__(self, processor, interval: int = 5):
        self.processor = processor
        self.interval = interval
        self.running = False
        self.logger = logging.getLogger(__name__)

    async def start(self) -> None:
        self.running = True
        self.logger.info("Outbox worker iniciado")
        while self.running:
            try:
                processed = await self.processor.process_pending()
                if processed:
                    self.logger.info(
                        "%s: processados %s eventos", datetime.utcnow().isoformat(), processed
                    )
                await asyncio.sleep(self.interval)
            except Exception as exc:
                self.logger.error("Erro OutboxWorker: %s", exc, exc_info=True)
                await asyncio.sleep(10)

    def stop(self) -> None:
        self.running = False


class EstatisticaWorker:
    def __init__(self, repo, interval: int = 60):
        self.repo = repo
        self.interval = interval
        self.running = False
        self.logger = logging.getLogger(__name__)

    async def start(self) -> None:
        self.running = True
        self.logger.info("Estatistica worker iniciado")
        while self.running:
            try:
                await self.repo.aggregate()
                await asyncio.sleep(self.interval)
            except Exception as exc:
                self.logger.error("Erro EstatisticaWorker: %s", exc, exc_info=True)
                await asyncio.sleep(30)

    def stop(self) -> None:
        self.running = False
