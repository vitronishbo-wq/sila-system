from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.economy.trade.external.application.ports import (
    DrawbackInternoRepositoryPort,
)
from apps.backend.app.modules.economy.trade.external.domain.models import DrawbackInterno
from apps.backend.app.modules.economy.trade.external.infrastructure.models import (
    DrawbackInternoModel,
)
from apps.backend.app.modules.economy.trade.external.infrastructure.repositories.sqlalchemy_habilitacao_repository_base import (
    SQLAlchemyHabilitacaoRepositoryBase,
)


class SQLAlchemyDrawbackInternoRepository(
    SQLAlchemyHabilitacaoRepositoryBase[DrawbackInterno, DrawbackInternoModel],
    DrawbackInternoRepositoryPort,
):
    def __init__(self, session: AsyncSession):
        super().__init__(session, model_cls=DrawbackInternoModel, domain_cls=DrawbackInterno)
