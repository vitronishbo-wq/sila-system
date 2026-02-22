from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_current_admin_user, get_db
from app.core.catalog.models.service import Service
from app.core.iam.models.user import User

router = APIRouter(prefix="/services", tags=["Services"])

@router.get("/")
async def list_public_services(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Service).where(Service.scope == "public", Service.is_active == True))
    services = result.scalars().all()
    return [{"id": str(s.id), "code": s.code, "name": s.name, "scope": s.scope} for s in services]

@router.get("/essential")
async def list_essential_services(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Service).where(
            Service.is_essential == True, 
            Service.is_active == True
        )
    )
    services = result.scalars().all()
    return [
        {
            "id": str(s.id), 
            "code": s.code, 
            "name": s.name, 
            "icon_slug": s.icon_slug
        } for s in services
    ]

@router.get("/private")
async def list_private_services(current_user: User = Depends(get_current_admin_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Service).where(Service.is_active == True))
    services = result.scalars().all()
    return [{"id": str(s.id), "code": s.code, "name": s.name, "scope": s.scope} for s in services]
