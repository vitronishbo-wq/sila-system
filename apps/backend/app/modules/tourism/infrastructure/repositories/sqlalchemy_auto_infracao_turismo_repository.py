from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.tourism.application.ports.auto_infracao_turismo_repository_port import AutoInfracaoTurismoRepositoryPort

class SQLAlchemyAutoInfracaoTurismoRepository(AutoInfracaoTurismoRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session
