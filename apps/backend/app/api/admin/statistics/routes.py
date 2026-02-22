from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_admin_user, get_db
from app.core.iam.models.user import User

router = APIRouter(prefix="/statistics", tags=["Statistics"])

@router.get("/")
async def statistics_root():
    return {"message": "Statistics API", "endpoints": ["/tree"]}

@router.get("/tree")
async def get_stat_tree(current_user: User = Depends(get_current_admin_user), db: AsyncSession = Depends(get_db)):
    return [{"id": "root", "name": "Angola", "type": "country", "children": []}]


