from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.economy.trade.external.application.ports import (
    HabilitacaoImportadorRepositoryPort,
)
from apps.backend.app.modules.economy.trade.external.domain.models import HabilitacaoImportador
from apps.backend.app.modules.economy.trade.external.infrastructure.models import (
    HabilitacaoImportadorModel,
)
from apps.backend.app.modules.economy.trade.external.infrastructure.repositories.sqlalchemy_habilitacao_repository_base import (
    SQLAlchemyHabilitacaoRepositoryBase,
)


class SQLAlchemyHabilitacaoImportadorRepository(
    SQLAlchemyHabilitacaoRepositoryBase[HabilitacaoImportador, HabilitacaoImportadorModel],
    HabilitacaoImportadorRepositoryPort,
):
    def __init__(self, session: AsyncSession):
        super().__init__(
            session, model_cls=HabilitacaoImportadorModel, domain_cls=HabilitacaoImportador
        )
