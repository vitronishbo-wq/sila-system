from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.turismo.application.ports.pacote_turistico_repository_port import PacoteTuristicoRepositoryPort


class SQLAlchemyPacoteTuristicoRepository(PacoteTuristicoRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session
