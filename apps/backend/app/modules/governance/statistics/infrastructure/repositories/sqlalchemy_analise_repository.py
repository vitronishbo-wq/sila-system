from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.governance.statistics.application.ports.analise_repository_port import AnaliseRepositoryPort
from app.modules.governance.statistics.infrastructure.models.analise_model import AnaliseModel
from app.modules.governance.statistics.infrastructure.repositories.base_named_repository import SQLAlchemyNamedRepository

class SQLAlchemyAnaliseRepository(SQLAlchemyNamedRepository, AnaliseRepositoryPort):

    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model_cls=AnaliseModel)