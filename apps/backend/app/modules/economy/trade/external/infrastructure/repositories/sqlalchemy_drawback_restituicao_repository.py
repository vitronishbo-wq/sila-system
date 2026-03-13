from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.economy.trade.external.application.ports import DrawbackRestituicaoRepositoryPort
from app.modules.economy.trade.external.domain.models import DrawbackRestituicao
from app.modules.economy.trade.external.infrastructure.models import DrawbackRestituicaoModel
from app.modules.economy.trade.external.infrastructure.repositories.sqlalchemy_habilitacao_repository_base import SQLAlchemyHabilitacaoRepositoryBase

class SQLAlchemyDrawbackRestituicaoRepository(SQLAlchemyHabilitacaoRepositoryBase[DrawbackRestituicao, DrawbackRestituicaoModel], DrawbackRestituicaoRepositoryPort):

    def __init__(self, session: AsyncSession):
        super().__init__(session, model_cls=DrawbackRestituicaoModel, domain_cls=DrawbackRestituicao)