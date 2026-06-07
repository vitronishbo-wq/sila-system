from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.tourism.application.ports.ponto_turistico_repository_port import (
    PontoTuristicoRepositoryPort,
)


class SQLAlchemyPontoTuristicoRepository(PontoTuristicoRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session
