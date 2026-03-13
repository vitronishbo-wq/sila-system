from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.tourism.application.ports.ocupacao_hoteleira_repository_port import OcupacaoHoteleiraRepositoryPort

class SQLAlchemyOcupacaoHoteleiraRepository(OcupacaoHoteleiraRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session
