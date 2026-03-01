from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.turismo.application.ports.classificacao_hoteleira_repository_port import ClassificacaoHoteleiraRepositoryPort


class SQLAlchemyClassificacaoHoteleiraRepository(ClassificacaoHoteleiraRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session
