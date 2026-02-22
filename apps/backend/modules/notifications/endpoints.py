from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from apps.backend.database.session import get_db
from apps.backend.modules.identity.auth import get_current_user
from apps.backend.modules.identity.models.user import User
from .models.notification import Notification

router = APIRouter()

@router.get("/me")
async def get_my_notifications_count(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        query = select(func.count(Notification.id)).where(
            Notification.user_id == current_user.id,
            Notification.status != "read"
        )
        result = await db.execute(query)
        count = result.scalar() or 0
        return {"unread_count": count}
    except Exception as e:
        return {"unread_count": 0}

@router.get("/")
async def list_my_notifications(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(Notification).where(
        Notification.user_id == current_user.id
    ).order_by(Notification.created_at.desc())
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/{notification_id}/read")
async def mark_as_read(
    notification_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(Notification).where(
        Notification.id == notification_id,
        Notification.user_id == current_user.id
    )
    result = await db.execute(query)
    notification = result.scalar_one_or_none()
    if not notification:
        raise HTTPException(status_code=404, detail="Notificação não encontrada")
    notification.status = "read"
    await db.commit()
    return {"status": "success"}