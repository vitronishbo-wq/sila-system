from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.turismo.application.ports.registro_guia_repository_port import RegistroGuiaRepositoryPort


class SQLAlchemyRegistroGuiaRepository(RegistroGuiaRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session
