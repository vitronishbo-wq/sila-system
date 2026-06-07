from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.core.database.session import AsyncSessionLocal
from apps.backend.app.modules.educacao.api.schemas.academic_wallet_schema import (
    AcademicWalletResponse,
)
from apps.backend.app.modules.educacao.application.academic_wallet_service import (
    AcademicWalletService,
)

router = APIRouter(prefix="/wallet", tags=["Academic Wallet"])


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@router.get("/{identity_id}", response_model=AcademicWalletResponse)
async def academic_wallet(
    identity_id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
):
    """Get unified student profile: identity, enrollments, record, guardians."""
    svc = AcademicWalletService(session)
    wallet = await svc.get_wallet(identity_id)
    if "error" in wallet:
        raise HTTPException(404, detail="Student not found")
    return AcademicWalletResponse(**wallet)
