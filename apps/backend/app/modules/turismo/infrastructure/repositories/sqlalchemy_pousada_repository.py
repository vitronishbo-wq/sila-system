from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.turismo.application.ports.pousada_repository_port import PousadaRepositoryPort


class SQLAlchemyPousadaRepository(PousadaRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session
