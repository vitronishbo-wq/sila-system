from __future__ import annotations

from typing import Generic, TypeVar
from uuid import UUID

from apps.backend.app.modules.economy.trade.external.application.ports import (
    HabilitacaoRepositoryPortBase,
)
from apps.backend.app.modules.economy.trade.external.domain.enums import StatusHabilitacao
from apps.backend.app.modules.economy.trade.external.domain.models import HabilitacaoBase

THabilitacao = TypeVar("THabilitacao", bound=HabilitacaoBase)


class InMemoryHabilitacaoRepositoryBase(
    HabilitacaoRepositoryPortBase[THabilitacao], Generic[THabilitacao]
):
    def __init__(self) -> None:
        self._items: dict[UUID, THabilitacao] = {}

    async def save(self, habilitacao: THabilitacao) -> THabilitacao:
        self._items[habilitacao.id] = habilitacao
        return habilitacao

    async def get_by_id(self, id: UUID) -> THabilitacao | None:
        return self._items.get(id)

    async def get_by_numero_processo(self, numero_processo: str) -> THabilitacao | None:
        lookup = numero_processo.strip()
        for item in self._items.values():
            if item.numero_processo == lookup:
                return item
        return None

    async def list(self, *, status: StatusHabilitacao | None = None) -> list[THabilitacao]:
        values = list(self._items.values())
        if status is not None:
            values = [item for item in values if item.status == status]
        values.sort(key=lambda item: item.data_solicitacao, reverse=True)
        return values
