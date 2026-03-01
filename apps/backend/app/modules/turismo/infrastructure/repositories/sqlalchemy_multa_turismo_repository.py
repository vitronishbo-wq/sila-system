from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.turismo.application.ports.multa_turismo_repository_port import MultaTurismoRepositoryPort


class SQLAlchemyMultaTurismoRepository(MultaTurismoRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session
