from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.economy.trade.external.application.ports import DrawbackIntegradoRepositoryPort
from app.modules.economy.trade.external.domain.models import DrawbackIntegrado
from app.modules.economy.trade.external.infrastructure.models import DrawbackIntegradoModel
from app.modules.economy.trade.external.infrastructure.repositories.sqlalchemy_habilitacao_repository_base import SQLAlchemyHabilitacaoRepositoryBase

class SQLAlchemyDrawbackIntegradoRepository(SQLAlchemyHabilitacaoRepositoryBase[DrawbackIntegrado, DrawbackIntegradoModel], DrawbackIntegradoRepositoryPort):

    def __init__(self, session: AsyncSession):
        super().__init__(session, model_cls=DrawbackIntegradoModel, domain_cls=DrawbackIntegrado)