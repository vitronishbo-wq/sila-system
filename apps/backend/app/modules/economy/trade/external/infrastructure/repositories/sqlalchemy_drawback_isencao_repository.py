from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.economy.trade.external.application.ports import DrawbackIsencaoRepositoryPort
from app.modules.economy.trade.external.domain.models import DrawbackIsencao
from app.modules.economy.trade.external.infrastructure.models import DrawbackIsencaoModel
from app.modules.economy.trade.external.infrastructure.repositories.sqlalchemy_habilitacao_repository_base import SQLAlchemyHabilitacaoRepositoryBase

class SQLAlchemyDrawbackIsencaoRepository(SQLAlchemyHabilitacaoRepositoryBase[DrawbackIsencao, DrawbackIsencaoModel], DrawbackIsencaoRepositoryPort):

    def __init__(self, session: AsyncSession):
        super().__init__(session, model_cls=DrawbackIsencaoModel, domain_cls=DrawbackIsencao)