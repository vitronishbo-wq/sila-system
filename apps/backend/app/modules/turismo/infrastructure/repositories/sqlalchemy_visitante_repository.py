from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.turismo.application.ports.visitante_repository_port import VisitanteRepositoryPort


class SQLAlchemyVisitanteRepository(VisitanteRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session
