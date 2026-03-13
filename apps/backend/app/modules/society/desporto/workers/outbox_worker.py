from __future__ import annotations
import asyncio
import os
import socket
from datetime import datetime, timezone
from app.modules.society.desporto.application.events import EventBus, event_bus as default_event_bus
from app.modules.society.desporto.application.ports.outbox_repository_port import OutboxRepositoryPort

class OutboxWorker:

    def __init__(self, *, outbox_repo: OutboxRepositoryPort, event_bus: EventBus | None=None, interval_seconds: float=1.0, batch_size: int=100, lock_ttl_seconds: int=60, retry_delay_seconds: int=5, worker_id: str | None=None) -> None:
        self.outbox_repo = outbox_repo
        self.event_bus = event_bus or default_event_bus
        self.interval_seconds = interval_seconds
        self.batch_size = batch_size
        self.lock_ttl_seconds = lock_ttl_seconds
        self.retry_delay_seconds = retry_delay_seconds
        self.worker_id = worker_id or f'{socket.gethostname()}-{os.getpid()}'
        self.running = False
        self.stats: dict[str, int | str | None] = {'processed': 0, 'failed': 0, 'last_batch_at': None}

    async def process_once(self) -> int:
        messages = await self.outbox_repo.pop_batch(self.batch_size, worker_id=self.worker_id, lock_ttl_seconds=self.lock_ttl_seconds)
        if not messages:
            return 0
        processed = 0
        for message in messages:
            try:
                await self.event_bus.publish(message.event)
                await self.outbox_repo.mark_processed(message)
                processed += 1
                self.stats['processed'] = int(self.stats['processed']) + 1
            except Exception as exc:
                await self.outbox_repo.mark_failed(message, error=str(exc), retry_delay_seconds=self.retry_delay_seconds)
                self.stats['failed'] = int(self.stats['failed']) + 1
        self.stats['last_batch_at'] = datetime.now(timezone.utc).isoformat()
        return processed

    async def run_forever(self) -> None:
        self.running = True
        while self.running:
            await self.process_once()
            await asyncio.sleep(self.interval_seconds)

    def stop(self) -> None:
        self.running = False