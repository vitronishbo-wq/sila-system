from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.economy.trade.external.application.ports import DrawbackSubstituicaoRepositoryPort
from apps.backend.app.modules.economy.trade.external.domain.models import DrawbackSubstituicao
from apps.backend.app.modules.economy.trade.external.infrastructure.models import DrawbackSubstituicaoModel
from apps.backend.app.modules.economy.trade.external.infrastructure.repositories.sqlalchemy_habilitacao_repository_base import SQLAlchemyHabilitacaoRepositoryBase

class SQLAlchemyDrawbackSubstituicaoRepository(SQLAlchemyHabilitacaoRepositoryBase[DrawbackSubstituicao, DrawbackSubstituicaoModel], DrawbackSubstituicaoRepositoryPort):

    def __init__(self, session: AsyncSession):
        super().__init__(session, model_cls=DrawbackSubstituicaoModel, domain_cls=DrawbackSubstituicao)