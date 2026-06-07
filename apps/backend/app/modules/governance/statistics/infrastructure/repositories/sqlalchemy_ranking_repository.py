from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.governance.statistics.application.ports.ranking_repository_port import (
    RankingRepositoryPort,
)
from apps.backend.app.modules.governance.statistics.infrastructure.models.ranking_model import (
    RankingModel,
)
from apps.backend.app.modules.governance.statistics.infrastructure.repositories.base_named_repository import (
    SQLAlchemyNamedRepository,
)


class SQLAlchemyRankingRepository(SQLAlchemyNamedRepository, RankingRepositoryPort):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model_cls=RankingModel)
