from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.tourism.application.ports.fiscalizacao_turismo_repository_port import (
    FiscalizacaoTurismoRepositoryPort,
)


class SQLAlchemyFiscalizacaoTurismoRepository(FiscalizacaoTurismoRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session
