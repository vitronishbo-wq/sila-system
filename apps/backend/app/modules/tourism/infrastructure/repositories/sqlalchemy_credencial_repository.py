from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.tourism.application.ports.credencial_repository_port import CredencialRepositoryPort

class SQLAlchemyCredencialRepository(CredencialRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session
