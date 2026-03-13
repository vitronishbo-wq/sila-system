"""Event Bus Bridge - atomic outbox + event store."""
import logging
from typing import Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.events.bus_enhanced import EventBus as _EnhancedBus
from app.core.events.models.event import DomainEvent
from app.core.events.outbox.outbox_repository import OutboxRepository
from app.core.events.store.repositories import EventStoreRepository
logger = logging.getLogger('events.bridge')

class EventBusEnhanced:
    """Lightweight wrapper for Enhanced Event Bus."""

    def __init__(self, db: Optional[AsyncSession]=None):
        self.db = db

    async def publish(self, event: DomainEvent) -> None:
        await _EnhancedBus.publish(event)

class EventBusBridge:
    """Bridge that persists to Outbox and Event Store in a single transaction."""

    def __init__(self, db_session: Optional[AsyncSession]=None):
        self.db = db_session
        self.outbox_repo = OutboxRepository(db_session) if db_session else None
        self.event_store_repo = EventStoreRepository(db_session) if db_session else None

    async def publish_atomic(self, event: DomainEvent, aggregate_id: Optional[Any]=None, aggregate_type: Optional[str]=None, version: Optional[int]=None, metadata: Optional[dict]=None) -> Optional[dict]:
        if not self.db:
            logger.warning('event_bus_bridge_missing_db')
            return None
        event_payload = event.to_dict() if hasattr(event, 'to_dict') else event
        if isinstance(event_payload, dict):
            event_name = event_payload.get('name')
            event_id = event_payload.get('id')
            payload = event_payload.get('payload', {})
        else:
            event_name = getattr(event, 'name', None)
            event_id = getattr(event, 'id', None)
            payload = getattr(event, 'payload', {})
        try:
            if self.outbox_repo:
                await self.outbox_repo.save(event_name=event_name, event_id=event_id, payload=event_payload)
            if self.event_store_repo and aggregate_id is not None:
                await self.event_store_repo.append(aggregate_id=aggregate_id, aggregate_type=aggregate_type or 'Unknown', event_type=event_name or 'UNKNOWN_EVENT', version=version or 1, payload=payload or {}, event_metadata=metadata)
            await self.db.commit()
            return event_payload
        except Exception as exc:
            await self.db.rollback()
            logger.error('event_bus_bridge_publish_failed', extra={'error': str(exc), 'event': event_name})
            raise