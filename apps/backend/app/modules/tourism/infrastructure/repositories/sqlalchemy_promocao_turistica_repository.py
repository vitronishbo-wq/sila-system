from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.tourism.application.ports.promocao_turistica_repository_port import PromocaoTuristicaRepositoryPort

class SQLAlchemyPromocaoTuristicaRepository(PromocaoTuristicaRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session
