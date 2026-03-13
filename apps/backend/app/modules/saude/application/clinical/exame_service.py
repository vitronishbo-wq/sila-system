from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession


class ExameService:
    """Servicos de exames (stub inicial)."""

    def __init__(self, session: AsyncSession | None = None) -> None:
        self._session = session

    async def get_laboratorial(self, exame_id) -> None:
        return None

    async def get_imagem(self, exame_id) -> None:
        return None
