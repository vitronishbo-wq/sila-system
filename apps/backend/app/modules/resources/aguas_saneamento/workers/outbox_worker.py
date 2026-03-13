from __future__ import annotations
import asyncio
from app.modules.resources.aguas_saneamento.application.bus import EventBus
from app.modules.resources.aguas_saneamento.application.events.registry import deserialize_event
from app.modules.resources.aguas_saneamento.application.ports.outbox_repository_port import OutboxRepositoryPort

class OutboxWorker:

    def __init__(self, *, outbox_repo: OutboxRepositoryPort, event_bus: EventBus) -> None:
        self._outbox_repo = outbox_repo
        self._event_bus = event_bus

    async def process_once(self, *, limit: int=100) -> int:
        processed = 0
        try:
            messages = await self._outbox_repo.get_pending(limit=limit)
        except Exception:
            return 0
        for message in messages:
            try:
                event = deserialize_event(message.event_name, message.payload)
                await self._event_bus.publish(event)
                await self._outbox_repo.mark_done(message.id)
                processed += 1
            except Exception as exc:
                await self._outbox_repo.increment_retries(message.id, error=str(exc))
        return processed

    async def run_forever(self, *, interval_seconds: float=1.0) -> None:
        while True:
            await self.process_once()
            await asyncio.sleep(interval_seconds)