from __future__ import annotations
from uuid import UUID
from sqlalchemy import func, select
from apps.backend.app.modules.society.familia.application.ports.outbox_repository_port import OutboxRepositoryPort
from apps.backend.app.modules.society.familia.infrastructure.models.event_outbox_model import FamilyOutboxEventModel

class OutboxRepository(OutboxRepositoryPort):

    def __init__(self, session) -> None:
        self._session = session

    async def store_many(self, events: list[object]) -> None:
        versions_cache: dict[UUID, int] = {}
        for event in events:
            payload = event.to_payload() if hasattr(event, 'to_payload') else {'raw': str(event)}
            aggregate_id = payload.get('aggregate_id')
            if aggregate_id is None:
                continue
            aggregate_uuid = UUID(str(aggregate_id))
            if aggregate_uuid not in versions_cache:
                current = await self._session.execute(select(func.max(FamilyOutboxEventModel.event_version)).where(FamilyOutboxEventModel.aggregate_id == aggregate_uuid))
                versions_cache[aggregate_uuid] = int(current.scalar_one() or 0)
            versions_cache[aggregate_uuid] += 1
            self._session.add(FamilyOutboxEventModel(aggregate_id=aggregate_uuid, event_type=getattr(event, 'event_name', event.__class__.__name__), event_version=versions_cache[aggregate_uuid], event_payload=payload, published=False))
        await self._session.flush()