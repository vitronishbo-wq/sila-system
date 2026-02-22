from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Dict

from apps.backend.database.session import get_db
from apps.backend.modules.identity.auth import get_current_user
from apps.backend.modules.identity.models.user import User
from .models.notification import Notification, NotificationStatus
from .services.notification_service import NotificationService

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("/me")
async def get_my_notifications_count(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Retorna o número de notificações não lidas para o Header do Frontend.
    """
    try:
        query = select(func.count(Notification.id)).where(
            Notification.user_id == current_user.id,
            Notification.status != "read" # Ajuste conforme o Enum NotificationStatus
        )
        result = await db.execute(query)
        count = result.scalar() or 0
        
        return {"unread_count": count}
    except Exception as e:
        print(f"Erro ao contar notificações: {e}")
        return {"unread_count": 0}

@router.get("/list")
async def list_my_notifications(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    limit: int = 10
):
    """
    Lista as últimas notificações do usuário.
    """
    query = select(Notification).where(
        Notification.user_id == current_user.id
    ).order_by(Notification.created_at.desc()).limit(limit)
    
    result = await db.execute(query)
    notifications = result.scalars().all()
    
    return notifications

@router.post("/{notification_id}/read")
async def mark_as_read(
    notification_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Marca uma notificação específica como lida.
    """
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