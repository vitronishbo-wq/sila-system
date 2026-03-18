from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.economy.trade.external.application.ports import CancelamentoRadarRepositoryPort
from apps.backend.app.modules.economy.trade.external.domain.models import CancelamentoRadar
from apps.backend.app.modules.economy.trade.external.infrastructure.models import CancelamentoRadarModel
from apps.backend.app.modules.economy.trade.external.infrastructure.repositories.sqlalchemy_habilitacao_repository_base import SQLAlchemyHabilitacaoRepositoryBase

class SQLAlchemyCancelamentoRadarRepository(SQLAlchemyHabilitacaoRepositoryBase[CancelamentoRadar, CancelamentoRadarModel], CancelamentoRadarRepositoryPort):

    def __init__(self, session: AsyncSession):
        super().__init__(session, model_cls=CancelamentoRadarModel, domain_cls=CancelamentoRadar)