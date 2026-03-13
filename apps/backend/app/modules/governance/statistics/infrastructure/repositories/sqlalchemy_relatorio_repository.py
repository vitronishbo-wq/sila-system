from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.governance.statistics.application.ports.relatorio_repository_port import RelatorioRepositoryPort
from app.modules.governance.statistics.infrastructure.models.relatorio_model import RelatorioModel
from app.modules.governance.statistics.infrastructure.repositories.base_named_repository import SQLAlchemyNamedRepository

class SQLAlchemyRelatorioRepository(SQLAlchemyNamedRepository, RelatorioRepositoryPort):

    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model_cls=RelatorioModel)