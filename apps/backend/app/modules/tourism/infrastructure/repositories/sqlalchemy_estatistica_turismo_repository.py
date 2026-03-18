from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.tourism.application.ports.estatistica_turismo_repository_port import EstatisticaTurismoRepositoryPort

class SQLAlchemyEstatisticaTurismoRepository(EstatisticaTurismoRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session