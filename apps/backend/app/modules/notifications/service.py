from __future__ import annotations
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.notifications.models import Notification

async def list_notifications(citizen_id: str, session: AsyncSession) -> list[Notification]:
    result = await session.execute(select(Notification).where(Notification.citizen_id == citizen_id))
    return list(result.scalars().all())
__all__ = ['list_notifications']