from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.events.store.event_repository import EventRepository

class EventStore:

    def __init__(self, db: AsyncSession):
        self.repo = EventRepository(db)

    async def append(self, event) -> None:
        await self.repo.save(event)

    async def load_stream(self, aggregate_id):
        return await self.repo.get_stream(aggregate_id)