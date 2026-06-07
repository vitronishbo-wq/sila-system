from __future__ import annotations

from datetime import date
from uuid import UUID

from apps.backend.app.modules.resources.ambiente.application.ports.imovel_repository_port import (
    ImovelRepositoryPort,
)
from apps.backend.app.modules.resources.ambiente.domain.models.imovel_rural import ImovelRural


class SQLAlchemyImovelRepository(ImovelRepositoryPort):
    """In-memory implementation with SQLAlchemy naming for progressive migration."""

    def __init__(self) -> None:
        self._items: dict[UUID, ImovelRural] = {}
        self._seq = 0

    async def save(self, item: ImovelRural) -> ImovelRural:
        self._items[item.id] = item
        return item

    async def get_by_id(self, imovel_id: UUID) -> ImovelRural | None:
        return self._items.get(imovel_id)

    async def get_by_codigo(self, codigo_imovel: str) -> ImovelRural | None:
        for item in self._items.values():
            if item.codigo_imovel == codigo_imovel:
                return item
        return None

    async def list_by_proprietario(self, proprietario_id: UUID) -> list[ImovelRural]:
        return [item for item in self._items.values() if item.proprietario_id == proprietario_id]

    async def next_codigo(self) -> str:
        self._seq += 1
        return f"IMV/{date.today().year}/{self._seq:06d}"
