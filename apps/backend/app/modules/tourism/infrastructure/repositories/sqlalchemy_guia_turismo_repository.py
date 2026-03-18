from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.tourism.application.ports.guia_turismo_repository_port import GuiaTurismoRepositoryPort

class SQLAlchemyGuiaTurismoRepository(GuiaTurismoRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session