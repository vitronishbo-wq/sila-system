from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.turismo.application.ports.agencia_viagens_repository_port import AgenciaViagensRepositoryPort


class SQLAlchemyAgenciaViagensRepository(AgenciaViagensRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session
