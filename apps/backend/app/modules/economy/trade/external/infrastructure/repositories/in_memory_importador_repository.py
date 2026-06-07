from __future__ import annotations

from uuid import UUID

from apps.backend.app.modules.economy.trade.external.application.ports import (
    ImportadorRepositoryPort,
)
from apps.backend.app.modules.economy.trade.external.domain.enums import StatusHabilitacao
from apps.backend.app.modules.economy.trade.external.domain.models import Importador


class InMemoryImportadorRepository(ImportadorRepositoryPort):
    def __init__(self) -> None:
        self._items: dict[UUID, Importador] = {}

    async def save(self, importador: Importador) -> Importador:
        self._items[importador.id] = importador
        return importador

    async def get_by_id(self, id: UUID) -> Importador | None:
        return self._items.get(id)

    async def get_by_cnpj_cpf(self, cnpj_cpf: str) -> Importador | None:
        lookup = cnpj_cpf.strip()
        for item in self._items.values():
            if item.cnpj_cpf == lookup:
                return item
        return None

    async def list(
        self, *, status: StatusHabilitacao | None = None, municipio: str | None = None
    ) -> list[Importador]:
        values = list(self._items.values())
        if status is not None:
            values = [item for item in values if item.status == status]
        if municipio is not None:
            values = [item for item in values if item.municipio.lower() == municipio.lower()]
        values.sort(key=lambda item: item.razao_social.lower())
        return values
