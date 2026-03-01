from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.turismo.application.ports.atracao_turistica_repository_port import AtracaoTuristicaRepositoryPort


class SQLAlchemyAtracaoTuristicaRepository(AtracaoTuristicaRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session
