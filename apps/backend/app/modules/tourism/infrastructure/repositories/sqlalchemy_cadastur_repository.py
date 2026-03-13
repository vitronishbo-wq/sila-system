from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.tourism.application.ports.cadastur_repository_port import CadasturRepositoryPort

class SQLAlchemyCadasturRepository(CadasturRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session
