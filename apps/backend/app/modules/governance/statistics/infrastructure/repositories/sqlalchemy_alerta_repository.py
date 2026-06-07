from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.governance.statistics.application.ports.alerta_repository_port import (
    AlertaRepositoryPort,
)
from apps.backend.app.modules.governance.statistics.infrastructure.models.alerta_model import (
    AlertaModel,
)
from apps.backend.app.modules.governance.statistics.infrastructure.repositories.base_named_repository import (
    SQLAlchemyNamedRepository,
)


class SQLAlchemyAlertaRepository(SQLAlchemyNamedRepository, AlertaRepositoryPort):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model_cls=AlertaModel)
