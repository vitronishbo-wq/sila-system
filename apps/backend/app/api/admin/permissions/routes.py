from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_admin_user, get_db
from app.core.iam.models.permissions import Permission
from modules.identity.models.user import User

router = APIRouter(prefix="/permissions", tags=["Permissions"])

@router.get("/")
async def get_permissions(current_user: User = Depends(get_current_admin_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Permission))
    permissions = result.scalars().all()
    return [
        {
            "id": p.id,
            "role": p.role,
            "service_code": p.service_code,
            "can_read": p.can_read,
            "can_write": p.can_write,
            "can_approve": p.can_approve,
        }
        for p in permissions
    ]
