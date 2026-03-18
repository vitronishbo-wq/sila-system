from __future__ import annotations
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_user, get_db
from app.modules.notifications.schemas import NotificationOut
from app.modules.notifications.service import list_notifications
router = APIRouter(tags=['notifications'])

@router.get('/notifications', response_model=list[NotificationOut])
async def get_notifications(user: dict=Depends(get_current_user), db: AsyncSession=Depends(get_db)):
    citizen_id = user.get('citizen_id') or user.get('sub')
    return await list_notifications(citizen_id, db)
__all__ = ['router']