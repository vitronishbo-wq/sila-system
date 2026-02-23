from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_current_citizen_user, get_db
from modules.identity.models.user import User
from app.core.notifications.models.notification import Notification

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("/")
async def list_notifications(
    current_user: User = Depends(get_current_citizen_user),
    db: AsyncSession = Depends(get_db)
):
    """Lista notificações do utilizador atual"""
    result = await db.execute(
        select(Notification)
        .where(Notification.user_id == current_user.id)
        .order_by(Notification.created_at.desc())
        .limit(100)
    )
    notifications = result.scalars().all()
    
    return [
        {
            "id": str(n.id),
            "title": n.title,
            "message": n.message,
            "type": n.notification_type,
            "is_read": n.is_read,
            "created_at": str(n.created_at),
            "document_id": str(n.document_id) if n.document_id else None
        }
        for n in notifications
    ]


@router.get("/unread-count")
async def get_unread_count(
    current_user: User = Depends(get_current_citizen_user),
    db: AsyncSession = Depends(get_db)
):
    """Conta notificações não lidas"""
    result = await db.execute(
        select(func.count(Notification.id))
        .where(Notification.user_id == current_user.id)
        .where(Notification.is_read == False)
    )
    count = result.scalar()
    
    return {"unread_count": count or 0}


@router.post("/{notification_id}/read")
async def mark_as_read(
    notification_id: str,
    current_user: User = Depends(get_current_citizen_user),
    db: AsyncSession = Depends(get_db)
):
    """Marca uma notificação como lida"""
    try:
        nid = UUID(notification_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="ID inválido")
    
    result = await db.execute(
        select(Notification)
        .where(Notification.id == nid)
        .where(Notification.user_id == current_user.id)
    )
    notification = result.scalar_one_or_none()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notificação não encontrada")
    
    notification.is_read = True
    notification.read_at = datetime.utcnow()
    await db.commit()
    
    return {"id": str(nid), "is_read": True, "message": "Notificação marcada como lida"}


@router.post("/read-all")
async def mark_all_as_read(
    current_user: User = Depends(get_current_citizen_user),
    db: AsyncSession = Depends(get_db)
):
    """Marca todas as notificações como lidas"""
    await db.execute(
        update(Notification)
        .where(Notification.user_id == current_user.id)
        .where(Notification.is_read == False)
        .values(is_read=True, read_at=datetime.utcnow())
    )
    await db.commit()
    
    return {"message": "Todas as notificações foram marcadas como lidas"}


@router.delete("/{notification_id}")
async def delete_notification(
    notification_id: str,
    current_user: User = Depends(get_current_citizen_user),
    db: AsyncSession = Depends(get_db)
):
    """Elimina uma notificação"""
    try:
        nid = UUID(notification_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="ID inválido")
    
    result = await db.execute(
        select(Notification)
        .where(Notification.id == nid)
        .where(Notification.user_id == current_user.id)
    )
    notification = result.scalar_one_or_none()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notificação não encontrada")
    
    await db.delete(notification)
    await db.commit()
    
    return {"id": str(nid), "message": "Notificação eliminada com sucesso"}
