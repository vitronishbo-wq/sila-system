from __future__ import annotations
from uuid import UUID
from apps.backend.app.modules.governance.cooperacao_internacional.application.ports.acordo_repository_port import AcordoRepositoryPort
from apps.backend.app.modules.governance.cooperacao_internacional.domain.enums import StatusAcordo
from apps.backend.app.modules.governance.cooperacao_internacional.domain.models.acordo import Acordo

class InMemoryAcordoRepository(AcordoRepositoryPort):

    def __init__(self) -> None:
        self._items: dict[UUID, Acordo] = {}

    async def save(self, acordo: Acordo) -> Acordo:
        self._items[acordo.id] = acordo
        return acordo

    async def get_by_id(self, acordo_id: UUID) -> Acordo | None:
        return self._items.get(acordo_id)

    async def list_all(self) -> list[Acordo]:
        return list(self._items.values())

    async def find_em_vigor(self) -> list[Acordo]:
        return [item for item in self._items.values() if item.status == StatusAcordo.EM_VIGOR]