from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.economy.trade.external.application.ports import HabilitacaoRadarRepositoryPort
from app.modules.economy.trade.external.domain.models import HabilitacaoRadar
from app.modules.economy.trade.external.infrastructure.models import HabilitacaoRadarModel
from app.modules.economy.trade.external.infrastructure.repositories.sqlalchemy_habilitacao_repository_base import SQLAlchemyHabilitacaoRepositoryBase

class SQLAlchemyHabilitacaoRadarRepository(SQLAlchemyHabilitacaoRepositoryBase[HabilitacaoRadar, HabilitacaoRadarModel], HabilitacaoRadarRepositoryPort):

    def __init__(self, session: AsyncSession):
        super().__init__(session, model_cls=HabilitacaoRadarModel, domain_cls=HabilitacaoRadar)