from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.tourism.application.ports.pacote_turistico_repository_port import PacoteTuristicoRepositoryPort

class SQLAlchemyPacoteTuristicoRepository(PacoteTuristicoRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session
