from __future__ import annotations
from uuid import UUID
from apps.backend.app.modules.infrastructure_sector.aviacao_civil.application.ports.aeronave_repository_port import AeronaveRepositoryPort
from apps.backend.app.modules.infrastructure_sector.aviacao_civil.domain.models.aeronave import Aeronave

class InMemoryAeronaveRepository(AeronaveRepositoryPort):

    def __init__(self) -> None:
        self._items: dict[UUID, Aeronave] = {}

    async def save(self, aeronave: Aeronave) -> Aeronave:
        self._items[aeronave.id] = aeronave
        return aeronave

    async def get_by_id(self, aeronave_id: UUID) -> Aeronave | None:
        return self._items.get(aeronave_id)

    async def get_by_matricula(self, matricula: str) -> Aeronave | None:
        key = matricula.strip().upper()
        for item in self._items.values():
            if item.matricula == key:
                return item
        return None

    async def list_all(self) -> list[Aeronave]:
        return list(self._items.values())