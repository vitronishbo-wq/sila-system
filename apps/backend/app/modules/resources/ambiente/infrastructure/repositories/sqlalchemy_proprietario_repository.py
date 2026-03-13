from __future__ import annotations
from datetime import date
from uuid import UUID
from apps.backend.app.modules.resources.ambiente.application.ports.proprietario_repository_port import ProprietarioRepositoryPort
from apps.backend.app.modules.resources.ambiente.domain.models.proprietario import Proprietario

class SQLAlchemyProprietarioRepository(ProprietarioRepositoryPort):
    """In-memory implementation with SQLAlchemy naming for progressive migration."""

    def __init__(self) -> None:
        self._items: dict[UUID, Proprietario] = {}
        self._seq = 0

    async def save(self, item: Proprietario) -> Proprietario:
        self._items[item.id] = item
        return item

    async def get_by_id(self, proprietario_id: UUID) -> Proprietario | None:
        return self._items.get(proprietario_id)

    async def get_by_documento(self, documento: str) -> Proprietario | None:
        for item in self._items.values():
            if item.documento == documento:
                return item
        return None

    async def next_codigo(self) -> str:
        self._seq += 1
        return f'PRP/{date.today().year}/{self._seq:06d}'