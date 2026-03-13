from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.economy.trade.external.application.ports import SiscomexDrawbackRepositoryPort
from app.modules.economy.trade.external.domain.models import SiscomexDrawback
from app.modules.economy.trade.external.infrastructure.models import SiscomexDrawbackModel
from app.modules.economy.trade.external.infrastructure.repositories.sqlalchemy_habilitacao_repository_base import SQLAlchemyHabilitacaoRepositoryBase

class SQLAlchemySiscomexDrawbackRepository(SQLAlchemyHabilitacaoRepositoryBase[SiscomexDrawback, SiscomexDrawbackModel], SiscomexDrawbackRepositoryPort):

    def __init__(self, session: AsyncSession):
        super().__init__(session, model_cls=SiscomexDrawbackModel, domain_cls=SiscomexDrawback)