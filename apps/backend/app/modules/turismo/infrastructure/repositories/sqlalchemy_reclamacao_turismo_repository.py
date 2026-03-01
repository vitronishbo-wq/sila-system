from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.turismo.application.ports.reclamacao_turismo_repository_port import ReclamacaoTurismoRepositoryPort


class SQLAlchemyReclamacaoTurismoRepository(ReclamacaoTurismoRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session
