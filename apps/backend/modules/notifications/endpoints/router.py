from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.db.session import get_async_db
from core.security import get_current_user
from modules.identity.models.user import User
from ..services.notification_service import NotificationService
from ..models.notification import Notification

router = APIRouter(tags=["notifications"])


from sqlalchemy import select, func

@router.get("/me")
async def get_my_notifications(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 50,
):
    """Retorna notificações do usuário com contagem de não lidas."""
    result = await db.execute(
        select(Notification)
        .where(Notification.user_id == current_user.id)
        .order_by(Notification.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    notifications = result.scalars().all()
    
    unread = await db.scalar(
        select(func.count(Notification.id))
        .where(Notification.user_id == current_user.id, Notification.read == False)
    )
    
    return {
        "data": notifications,
        "unread_count": unread or 0
    }


@router.post("/dispatch")
async def manual_dispatch(
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_async_db),
):
    service = NotificationService(db)
    background_tasks.add_task(service.dispatch_pending)
    return {"detail": "Dispatch queued"}
