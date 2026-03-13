from __future__ import annotations
import asyncio
from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker
from app.domain.db import AsyncSessionLocal
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.events.bus import event_bus
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.events.registry import deserialize_event
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.infrastructure.persistence.outbox_model import OutboxEventModel

class OutboxWorker:

    def __init__(self, *, session_factory: async_sessionmaker | None=None, interval_seconds: float=1.0) -> None:
        self._session_factory = session_factory or AsyncSessionLocal
        self._interval_seconds = interval_seconds
        self._running = False

    async def process_once(self, *, limit: int=100) -> int:
        processed = 0
        async with self._session_factory() as session:
            result = await session.execute(select(OutboxEventModel).where(OutboxEventModel.processed.is_(False)).order_by(OutboxEventModel.created_at.asc()).limit(limit))
            rows = result.scalars().all()
            for row in rows:
                try:
                    event = deserialize_event(row.event_name, dict(row.payload or {}))
                    await event_bus.publish(event)
                    row.processed = True
                    row.processed_at = datetime.now(timezone.utc)
                    row.last_error = None
                    processed += 1
                except Exception as exc:
                    row.retries = int(row.retries or 0) + 1
                    row.last_error = str(exc)
            await session.commit()
        return processed

    async def run_forever(self) -> None:
        self._running = True
        while self._running:
            await self.process_once()
            await asyncio.sleep(self._interval_seconds)

    def stop(self) -> None:
        self._running = False

async def _run_worker_forever() -> None:
    worker = OutboxWorker()
    await worker.run_forever()
if __name__ == '__main__':
    asyncio.run(_run_worker_forever())