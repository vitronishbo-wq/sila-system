from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.governance.statistics.application.ports.exportacao_repository_port import ExportacaoRepositoryPort
from apps.backend.app.modules.governance.statistics.infrastructure.models.exportacao_model import ExportacaoModel
from apps.backend.app.modules.governance.statistics.infrastructure.repositories.base_named_repository import SQLAlchemyNamedRepository

class SQLAlchemyExportacaoRepository(SQLAlchemyNamedRepository, ExportacaoRepositoryPort):

    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model_cls=ExportacaoModel)