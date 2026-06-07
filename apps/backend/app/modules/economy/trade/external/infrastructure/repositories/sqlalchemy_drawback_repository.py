from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.economy.trade.external.application.ports import DrawbackRepositoryPort
from apps.backend.app.modules.economy.trade.external.domain.models import Drawback
from apps.backend.app.modules.economy.trade.external.infrastructure.models import DrawbackModel
from apps.backend.app.modules.economy.trade.external.infrastructure.repositories.sqlalchemy_operador_logistico_repository_base import (
    SQLAlchemyOperadorLogisticoRepositoryBase,
)


class SQLAlchemyDrawbackRepository(
    SQLAlchemyOperadorLogisticoRepositoryBase[Drawback, DrawbackModel], DrawbackRepositoryPort
):
    def __init__(self, session: AsyncSession):
        super().__init__(session, model_cls=DrawbackModel, domain_cls=Drawback)
