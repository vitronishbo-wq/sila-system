from __future__ import annotations

from uuid import UUID

from apps.backend.app.modules.resources.pescas.domain.models.fiscalizacao_pesca import (
    FiscalizacaoPesca,
)


class FiscalizacaoService:
    def __init__(self) -> None:
        self._items: dict[UUID, FiscalizacaoPesca] = {}

    async def registrar_fiscalizacao(
        self,
        *,
        embarcacao_id: UUID,
        local: str,
        agente: str,
        regular: bool,
        observacoes: str | None = None,
    ) -> FiscalizacaoPesca:
        item = FiscalizacaoPesca.registrar(
            embarcacao_id=embarcacao_id,
            local=local,
            agente=agente,
            regular=regular,
            observacoes=observacoes,
        )
        self._items[item.id] = item
        return item

    async def listar(self) -> list[FiscalizacaoPesca]:
        return list(self._items.values())
