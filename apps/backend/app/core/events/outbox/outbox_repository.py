"""Outbox Repository - Phase 19"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from datetime import datetime
from typing import List
from .outbox_model import OutboxEvent

class OutboxRepository:
    """Repository for outbox event persistence"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(self, event_name: str, event_id: str, payload: dict) -> OutboxEvent:
        """Save event to outbox"""
        record = OutboxEvent(event_name=event_name, event_id=event_id, payload=payload)
        self.db.add(record)
        await self.db.flush()
        return record

    async def get_unprocessed(self, limit: int=100) -> List[OutboxEvent]:
        """Get unprocessed events"""
        stmt = select(OutboxEvent).where(OutboxEvent.processed == False).limit(limit).order_by(OutboxEvent.created_at)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def mark_processed(self, event_id: str):
        """Mark event as processed"""
        stmt = update(OutboxEvent).where(OutboxEvent.id == event_id).values(processed=True, processed_at=datetime.utcnow())
        await self.db.execute(stmt)
        await self.db.commit()

    async def delete_processed(self, days_retention: int=7):
        """Delete processed events older than retention period"""
        from datetime import timedelta
        cutoff = datetime.utcnow() - timedelta(days=days_retention)
        stmt = select(OutboxEvent).where((OutboxEvent.processed == True) & (OutboxEvent.processed_at < cutoff))
        result = await self.db.execute(stmt)
        events = result.scalars().all()
        for event in events:
            await self.db.delete(event)
        await self.db.commit()
        return len(events)