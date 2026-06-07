from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.economy.trade.external.application.ports import (
    SuspensaoRadarRepositoryPort,
)
from apps.backend.app.modules.economy.trade.external.domain.models import SuspensaoRadar
from apps.backend.app.modules.economy.trade.external.infrastructure.models import (
    SuspensaoRadarModel,
)
from apps.backend.app.modules.economy.trade.external.infrastructure.repositories.sqlalchemy_habilitacao_repository_base import (
    SQLAlchemyHabilitacaoRepositoryBase,
)


class SQLAlchemySuspensaoRadarRepository(
    SQLAlchemyHabilitacaoRepositoryBase[SuspensaoRadar, SuspensaoRadarModel],
    SuspensaoRadarRepositoryPort,
):
    def __init__(self, session: AsyncSession):
        super().__init__(session, model_cls=SuspensaoRadarModel, domain_cls=SuspensaoRadar)
