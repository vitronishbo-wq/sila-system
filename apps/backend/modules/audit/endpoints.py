from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from core.db.session import get_async_db
from core.security import get_current_superuser
from modules.identity.models.user import User
from .models import AuditLog

router = APIRouter(prefix="/audit", tags=["Audit"])

@router.get("/admin", response_model=List[dict])
async def get_audit_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    action: Optional[str] = None,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_superuser),
):
    """
    Rastreabilidade Nacional - Visualização de Logs de Auditoria (Admin Only).
    """
    query = (
        select(AuditLog)
        .options(joinedload(AuditLog.user))
        .order_by(AuditLog.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    
    if action:
        query = query.where(AuditLog.action == action)
        
    result = await db.execute(query)
    logs = result.scalars().all()
    
    # Simple manual mapping to handle User relation in the response
    # In a real app, we'd use a Pydantic schema here.
    return [
        {
            "id": str(log.id),
            "user_id": str(log.user_id),
            "action": log.action,
            "resource_id": log.resource_id,
            "metadata_json": log.metadata_json,
            "created_at": log.created_at.isoformat(),
            "user": {
                "full_name": log.user.full_name,
                "email": log.user.email
            } if log.user else None
        }
        for log in logs
    ]
