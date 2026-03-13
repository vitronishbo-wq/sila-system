from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.tourism.application.ports.operador_turistico_repository_port import OperadorTuristicoRepositoryPort

class SQLAlchemyOperadorTuristicoRepository(OperadorTuristicoRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session
