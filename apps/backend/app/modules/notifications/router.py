from __future__ import annotations

from apps.backend.app.api.deps import get_current_user, get_db
from apps.backend.app.modules.notifications.schemas import NotificationOut
from apps.backend.app.modules.notifications.service import list_notifications
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(tags=["notifications"])


@router.get("/notifications", response_model=list[NotificationOut])
async def get_notifications(
    user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    citizen_id = user.get("citizen_id") or user.get("sub")
    return await list_notifications(citizen_id, db)


__all__ = ["router"]
