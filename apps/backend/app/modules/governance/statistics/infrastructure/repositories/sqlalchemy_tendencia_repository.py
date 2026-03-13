from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.governance.statistics.application.ports.tendencia_repository_port import TendenciaRepositoryPort
from app.modules.governance.statistics.infrastructure.models.tendencia_model import TendenciaModel
from app.modules.governance.statistics.infrastructure.repositories.base_named_repository import SQLAlchemyNamedRepository

class SQLAlchemyTendenciaRepository(SQLAlchemyNamedRepository, TendenciaRepositoryPort):

    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model_cls=TendenciaModel)