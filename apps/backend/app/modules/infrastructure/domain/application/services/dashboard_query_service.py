from __future__ import annotations
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.infrastructure.infrastructure.read_model.dashboard_model import ObraDashboardReadModel

class DashboardQueryService:

    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def listar_obras(self, *, tenant_id: str | None=None) -> list[ObraDashboardReadModel]:
        stmt = select(ObraDashboardReadModel).order_by(ObraDashboardReadModel.updated_at.desc())
        if tenant_id:
            stmt = stmt.where(ObraDashboardReadModel.tenant_id == tenant_id)
        result = await self._db.execute(stmt)
        return list(result.scalars().all())
