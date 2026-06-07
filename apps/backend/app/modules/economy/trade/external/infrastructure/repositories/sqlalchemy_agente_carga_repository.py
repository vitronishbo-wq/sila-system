from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.economy.trade.external.application.ports import (
    AgenteCargaRepositoryPort,
)
from apps.backend.app.modules.economy.trade.external.domain.models import AgenteCarga
from apps.backend.app.modules.economy.trade.external.infrastructure.models import AgenteCargaModel
from apps.backend.app.modules.economy.trade.external.infrastructure.repositories.sqlalchemy_operador_logistico_repository_base import (
    SQLAlchemyOperadorLogisticoRepositoryBase,
)


class SQLAlchemyAgenteCargaRepository(
    SQLAlchemyOperadorLogisticoRepositoryBase[AgenteCarga, AgenteCargaModel],
    AgenteCargaRepositoryPort,
):
    def __init__(self, session: AsyncSession):
        super().__init__(session, model_cls=AgenteCargaModel, domain_cls=AgenteCarga)
