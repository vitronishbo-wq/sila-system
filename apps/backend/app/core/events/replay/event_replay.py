from __future__ import annotations

from apps.backend.app.core.events.projection.projection_manager import ProjectionManager
from apps.backend.app.core.events.store.event_store import EventStore


class EventReplay:
    def __init__(self, store: EventStore):
        self.store = store

    async def rebuild_projection(self, aggregate_id):
        events = await self.store.load_stream(aggregate_id)
        for event_record in events:
            event = event_record.payload
            await ProjectionManager.apply(event)
