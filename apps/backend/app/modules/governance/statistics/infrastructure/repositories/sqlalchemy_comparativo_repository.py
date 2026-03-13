from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.governance.statistics.application.ports.comparativo_repository_port import ComparativoRepositoryPort
from apps.backend.app.modules.governance.statistics.infrastructure.models.comparativo_model import ComparativoModel
from apps.backend.app.modules.governance.statistics.infrastructure.repositories.base_named_repository import SQLAlchemyNamedRepository

class SQLAlchemyComparativoRepository(SQLAlchemyNamedRepository, ComparativoRepositoryPort):

    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model_cls=ComparativoModel)