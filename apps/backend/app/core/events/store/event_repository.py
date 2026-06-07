from __future__ import annotations

from typing import Any
from uuid import uuid4

from apps.backend.app.core.events.models.event import DomainEvent
from apps.backend.app.core.events.outbox.outbox_model import OutboxEvent
from sqlalchemy import select


class EventRepository:
    def __init__(self, db):
        self.db = db

    async def save(self, event: DomainEvent | dict[str, Any]) -> None:
        if isinstance(event, dict):
            event_name = event.get("name") or event.get("event_name") or "UNKNOWN_EVENT"
            event_id = event.get("id") or event.get("event_id") or str(uuid4())
            payload = event
        else:
            event_name = (
                getattr(event, "name", None)
                or getattr(event, "event_name", None)
                or "UNKNOWN_EVENT"
            )
            event_id = getattr(event, "id", None) or str(uuid4())
            if hasattr(event, "to_dict"):
                payload = event.to_dict()
            else:
                payload = dict(getattr(event, "__dict__", {}))
        record = OutboxEvent(event_name=event_name, event_id=str(event_id), payload=payload)
        self.db.add(record)

    async def get_stream(self, aggregate_id):
        query = select(OutboxEvent).where(
            OutboxEvent.payload["aggregate_id"].astext == str(aggregate_id)
        )
        result = await self.db.execute(query)
        return result.scalars().all()
