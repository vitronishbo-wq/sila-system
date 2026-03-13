from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.governance.statistics.application.ports.agregacao_repository_port import AgregacaoRepositoryPort
from app.modules.governance.statistics.infrastructure.models.agregacao_model import AgregacaoModel
from app.modules.governance.statistics.infrastructure.repositories.base_named_repository import SQLAlchemyNamedRepository

class SQLAlchemyAgregacaoRepository(SQLAlchemyNamedRepository, AgregacaoRepositoryPort):

    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model_cls=AgregacaoModel)