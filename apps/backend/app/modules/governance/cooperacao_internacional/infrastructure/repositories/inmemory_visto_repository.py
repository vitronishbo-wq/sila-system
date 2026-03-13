from __future__ import annotations
from uuid import UUID
from apps.backend.app.modules.governance.cooperacao_internacional.application.ports.visto_repository_port import VistoRepositoryPort
from apps.backend.app.modules.governance.cooperacao_internacional.domain.models.visto import Visto

class InMemoryVistoRepository(VistoRepositoryPort):

    def __init__(self) -> None:
        self._items: dict[UUID, Visto] = {}

    async def save(self, visto: Visto) -> Visto:
        self._items[visto.id] = visto
        return visto

    async def get_by_id(self, visto_id: UUID) -> Visto | None:
        return self._items.get(visto_id)

    async def list_all(self) -> list[Visto]:
        return list(self._items.values())