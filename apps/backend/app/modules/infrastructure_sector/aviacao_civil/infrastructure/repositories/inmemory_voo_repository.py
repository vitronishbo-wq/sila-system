from __future__ import annotations

from datetime import datetime
from uuid import UUID

from apps.backend.app.modules.infrastructure_sector.aviacao_civil.application.ports.voo_repository_port import (
    VooRepositoryPort,
)
from apps.backend.app.modules.infrastructure_sector.aviacao_civil.domain.enums import StatusVoo
from apps.backend.app.modules.infrastructure_sector.aviacao_civil.domain.models.voo import Voo


class InMemoryVooRepository(VooRepositoryPort):
    def __init__(self) -> None:
        self._items: dict[UUID, Voo] = {}

    async def save(self, voo: Voo) -> Voo:
        self._items[voo.id] = voo
        return voo

    async def get_by_id(self, voo_id: UUID) -> Voo | None:
        return self._items.get(voo_id)

    async def get_by_numero(self, numero_voo: str) -> Voo | None:
        key = numero_voo.strip().upper()
        for item in self._items.values():
            if item.numero_voo == key:
                return item
        return None

    async def list_all(self) -> list[Voo]:
        return list(self._items.values())

    async def find_by_status(self, status: StatusVoo) -> list[Voo]:
        return [item for item in self._items.values() if item.status == status]

    async def find_by_periodo(self, inicio: datetime, fim: datetime) -> list[Voo]:
        return [
            item
            for item in self._items.values()
            if inicio <= item.data_hora_partida_programada <= fim
        ]
