"""Event Bus Implementation - Phase 19"""
import logging
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.events.outbox.outbox_repository import OutboxRepository
from app.core.events.models.event import DomainEvent
logger = logging.getLogger('events.bus')

class EventBus:
    """Central event bus for publishing domain events"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.outbox_repo = OutboxRepository(db)

    async def publish(self, event: DomainEvent):
        """Transactionally publish event to outbox"""
        try:
            await self.outbox_repo.save(event_name=event.name, event_id=event.id, payload=event.to_dict())
            await self.db.commit()
            logger.info('event_published_to_outbox', extra={'event': event.name, 'event_id': event.id})
        except Exception as e:
            await self.db.rollback()
            logger.error('event_publish_error', extra={'error': str(e), 'event': event.name})
            raise