from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.tourism.application.ports.receita_turistica_repository_port import ReceitaTuristicaRepositoryPort

class SQLAlchemyReceitaTuristicaRepository(ReceitaTuristicaRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session
