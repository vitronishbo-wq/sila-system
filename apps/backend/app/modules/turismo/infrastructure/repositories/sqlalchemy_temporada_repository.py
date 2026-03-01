from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.turismo.application.ports.temporada_repository_port import TemporadaRepositoryPort


class SQLAlchemyTemporadaRepository(TemporadaRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session
