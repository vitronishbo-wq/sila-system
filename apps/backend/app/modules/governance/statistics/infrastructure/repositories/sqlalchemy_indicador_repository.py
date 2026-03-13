from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.governance.statistics.application.ports.indicador_repository_port import IndicadorRepositoryPort
from app.modules.governance.statistics.infrastructure.models.indicador_model import IndicadorModel
from app.modules.governance.statistics.infrastructure.repositories.base_named_repository import SQLAlchemyNamedRepository

class SQLAlchemyIndicadorRepository(SQLAlchemyNamedRepository, IndicadorRepositoryPort):

    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model_cls=IndicadorModel)