from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.turismo.application.ports.roteiro_repository_port import RoteiroRepositoryPort


class SQLAlchemyRoteiroRepository(RoteiroRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session
