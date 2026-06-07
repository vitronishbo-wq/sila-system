from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.governance.statistics.application.ports.previsao_repository_port import (
    PrevisaoRepositoryPort,
)
from apps.backend.app.modules.governance.statistics.infrastructure.models.previsao_model import (
    PrevisaoModel,
)
from apps.backend.app.modules.governance.statistics.infrastructure.repositories.base_named_repository import (
    SQLAlchemyNamedRepository,
)


class SQLAlchemyPrevisaoRepository(SQLAlchemyNamedRepository, PrevisaoRepositoryPort):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model_cls=PrevisaoModel)
