from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.tourism.application.ports.avaliacao_repository_port import AvaliacaoRepositoryPort

class SQLAlchemyAvaliacaoRepository(AvaliacaoRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session