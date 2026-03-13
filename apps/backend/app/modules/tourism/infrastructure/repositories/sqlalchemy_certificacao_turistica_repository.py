from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.tourism.application.ports.certificacao_turistica_repository_port import CertificacaoTuristicaRepositoryPort

class SQLAlchemyCertificacaoTuristicaRepository(CertificacaoTuristicaRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session
