from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.tourism.application.ports.cadastro_turista_repository_port import CadastroTuristaRepositoryPort

class SQLAlchemyCadastroTuristaRepository(CadastroTuristaRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session