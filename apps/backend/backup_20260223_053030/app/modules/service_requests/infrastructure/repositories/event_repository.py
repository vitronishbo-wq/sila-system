"""Event repository implementation"""
from typing import List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ...domain.models.request_event import RequestEvent
from ..models.request_event_model import RequestEventModel


class EventRepository:
    """Request event repository"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(self, event: RequestEvent) -> RequestEvent:
        """Save event"""
        model = RequestEventModel(
            id=event.id,
            request_id=event.request_id,
            event_type=event.event_type,
            payload=event.payload,
            actor_id=event.actor_id,
        )
        self.db.add(model)
        await self.db.flush()
        return event

    async def get_by_request(self, request_id: UUID) -> List[RequestEvent]:
        """Get all events for a request"""
        stmt = select(RequestEventModel).where(
            RequestEventModel.request_id == request_id
        ).order_by(RequestEventModel.created_at.asc())
        result = await self.db.execute(stmt)
        models = result.scalars().all()
        
        events = []
        for model in models:
            events.append(RequestEvent(
                id=model.id,
                request_id=model.request_id,
                event_type=model.event_type,
                payload=model.payload or {},
                actor_id=model.actor_id,
                created_at=model.created_at,
            ))
        
        return events

    async def get_recent(self, request_id: UUID, limit: int = 20) -> List[RequestEvent]:
        """Get recent events"""
        stmt = select(RequestEventModel).where(
            RequestEventModel.request_id == request_id
        ).order_by(RequestEventModel.created_at.desc()).limit(limit)
        result = await self.db.execute(stmt)
        models = result.scalars().all()
        
        events = []
        for model in reversed(models):
            events.append(RequestEvent(
                id=model.id,
                request_id=model.request_id,
                event_type=model.event_type,
                payload=model.payload or {},
                actor_id=model.actor_id,
                created_at=model.created_at,
            ))
        
        return events
