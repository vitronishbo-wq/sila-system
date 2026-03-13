from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.economy.trade.external.application.ports import HabilitacaoExportadorRepositoryPort
from app.modules.economy.trade.external.domain.models import HabilitacaoExportador
from app.modules.economy.trade.external.infrastructure.models import HabilitacaoExportadorModel
from app.modules.economy.trade.external.infrastructure.repositories.sqlalchemy_habilitacao_repository_base import SQLAlchemyHabilitacaoRepositoryBase

class SQLAlchemyHabilitacaoExportadorRepository(SQLAlchemyHabilitacaoRepositoryBase[HabilitacaoExportador, HabilitacaoExportadorModel], HabilitacaoExportadorRepositoryPort):

    def __init__(self, session: AsyncSession):
        super().__init__(session, model_cls=HabilitacaoExportadorModel, domain_cls=HabilitacaoExportador)