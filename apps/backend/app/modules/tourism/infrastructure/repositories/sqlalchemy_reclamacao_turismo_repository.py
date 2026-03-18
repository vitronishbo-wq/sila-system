from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.tourism.application.ports.reclamacao_turismo_repository_port import ReclamacaoTurismoRepositoryPort

class SQLAlchemyReclamacaoTurismoRepository(ReclamacaoTurismoRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session