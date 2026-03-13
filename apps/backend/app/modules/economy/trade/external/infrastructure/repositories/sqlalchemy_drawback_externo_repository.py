from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.economy.trade.external.application.ports import DrawbackExternoRepositoryPort
from app.modules.economy.trade.external.domain.models import DrawbackExterno
from app.modules.economy.trade.external.infrastructure.models import DrawbackExternoModel
from app.modules.economy.trade.external.infrastructure.repositories.sqlalchemy_habilitacao_repository_base import SQLAlchemyHabilitacaoRepositoryBase

class SQLAlchemyDrawbackExternoRepository(SQLAlchemyHabilitacaoRepositoryBase[DrawbackExterno, DrawbackExternoModel], DrawbackExternoRepositoryPort):

    def __init__(self, session: AsyncSession):
        super().__init__(session, model_cls=DrawbackExternoModel, domain_cls=DrawbackExterno)