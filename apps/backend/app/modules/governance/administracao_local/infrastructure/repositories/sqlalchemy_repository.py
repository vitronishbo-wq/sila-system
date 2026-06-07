from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.governance.administracao_local.domain.entities import (
    AdministradorLocal,
)
from apps.backend.app.modules.governance.administracao_local.infrastructure.mappers import (
    AdministradorMapper,
)
from apps.backend.app.modules.governance.administracao_local.infrastructure.models import (
    AdministradorModel,
)


class Repository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, admin_id: str) -> AdministradorLocal:
        result = await self.db.execute(
            select(AdministradorModel).where(AdministradorModel.id == admin_id)
        )
        model = result.scalar_one_or_none()
        if not model:
            return None
        return AdministradorMapper.to_domain(model)
