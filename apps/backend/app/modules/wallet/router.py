from __future__ import annotations

from apps.backend.app.api.deps import get_current_user, get_db
from apps.backend.app.modules.wallet.schemas import DocumentOut
from apps.backend.app.modules.wallet.service import get_documents
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(tags=["wallet"])


@router.get("/wallet", response_model=list[DocumentOut])
async def get_wallet(user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    citizen_id = user.get("citizen_id")
    if not citizen_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="citizen_id missing in token"
        )
    return await get_documents(citizen_id, db)


__all__ = ["router"]
