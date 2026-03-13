from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.economy.trade.external.application.ports import DrawbackSuspensaoRepositoryPort
from app.modules.economy.trade.external.domain.models import DrawbackSuspensao
from app.modules.economy.trade.external.infrastructure.models import DrawbackSuspensaoModel
from app.modules.economy.trade.external.infrastructure.repositories.sqlalchemy_habilitacao_repository_base import SQLAlchemyHabilitacaoRepositoryBase

class SQLAlchemyDrawbackSuspensaoRepository(SQLAlchemyHabilitacaoRepositoryBase[DrawbackSuspensao, DrawbackSuspensaoModel], DrawbackSuspensaoRepositoryPort):

    def __init__(self, session: AsyncSession):
        super().__init__(session, model_cls=DrawbackSuspensaoModel, domain_cls=DrawbackSuspensao)