# modules/statistics/endpoints/router.py
from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.session import get_async_db
from core.security import get_current_superuser
from modules.documents.models.documents import Document, DocumentStatus
from modules.identity.models.user import User


router = APIRouter(tags=["statistics"])


@router.get("/admin")
async def admin_statistics(
    db: AsyncSession = Depends(get_async_db),
    current_user=Depends(get_current_superuser),
):
    today = datetime.utcnow().date()

    # Totais gerais
    total_documents = await db.scalar(select(func.count(Document.id)))
    total_users = await db.scalar(select(func.count(User.id)))

    # Por status
    status_counts = await db.execute(
        select(Document.status, func.count(Document.id))
        .group_by(Document.status)
    )
    status_dict = {row[0]: row[1] for row in status_counts}

    # Hoje
    today_docs = await db.scalar(
        select(func.count(Document.id))
        .where(func.date(Document.created_at) == today)
    )

    # Volume de upload hoje (MB)
    today_volume = await db.scalar(
        select(func.sum(Document.file_size))
        .where(func.date(Document.created_at) == today)
    )
    today_volume_mb = round((today_volume or 0) / (1024 * 1024), 2)

    # Novos usuários hoje
    new_users_today = await db.scalar(
        select(func.count(User.id))
        .where(func.date(User.created_at) == today)
    )

    return {
        "total_documents": total_documents,
        "total_users": total_users,
        "documents_today": today_docs,
        "volume_today_mb": today_volume_mb,
        "new_users_today": new_users_today,
        "status_breakdown": {
            "pending": status_dict.get(DocumentStatus.PENDING.value, 0),
            "processing": status_dict.get(DocumentStatus.PROCESSING.value, 0),
            "completed": status_dict.get(DocumentStatus.COMPLETED.value, 0),
            "failed": status_dict.get(DocumentStatus.FAILED.value, 0),
        },
    }

from core.security import get_current_user

@router.get("/me")
async def my_statistics(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    """Estatísticas pessoais do cidadão"""
    
    # Meus documentos totais
    my_total_docs = await db.scalar(
        select(func.count(Document.id)).where(Document.owner_id == current_user.id)
    )
    
    # Meus documentos por status
    my_status_counts = await db.execute(
        select(Document.status, func.count(Document.id))
        .where(Document.owner_id == current_user.id)
        .group_by(Document.status)
    )
    my_status_dict = {row[0]: row[1] for row in my_status_counts}
    
    return {
        "total_documents": my_total_docs,
        "status_breakdown": {
            "pending": my_status_dict.get(DocumentStatus.PENDING.value, 0),
            "processing": my_status_dict.get(DocumentStatus.PROCESSING.value, 0),
            "completed": my_status_dict.get(DocumentStatus.COMPLETED.value, 0),
            "failed": my_status_dict.get(DocumentStatus.FAILED.value, 0),
        }
    }
