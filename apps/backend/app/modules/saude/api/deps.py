from __future__ import annotations

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.api.deps import get_db

session_dep = Depends(get_db)

from apps.backend.app.modules.saude.application.clinical.exame_service import ExameService


async def get_exame_service(session: AsyncSession = session_dep) -> ExameService:
    return ExameService(session=session)
