from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.api.deps import get_db, get_current_user
from app.core.workflow.models.request import Request
from modules.identity.models.user import User

router = APIRouter(prefix="/requests", tags=["admin-requests"])

@router.get("/")
async def list_requests(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
):
    """Lista real de pedidos da BD"""
    if current_user.role not in ["ADMIN_SUPER", "ADMIN_CENTRAL", "ADMIN_PROVINCIAL", "ADMIN_MUNICIPAL", "ADMIN_COMMUNAL"]:
        raise HTTPException(status_code=403, detail="Acesso negado")
    
    result = await db.execute(select(Request).offset(skip).limit(limit))
    requests = result.scalars().all()
    return requests

@router.get("/{request_id}")
async def get_request(
    request_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Busca pedido real da BD"""
    result = await db.execute(select(Request).filter(Request.id == request_id))
    request = result.scalar_one_or_none()
    if not request:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return request
