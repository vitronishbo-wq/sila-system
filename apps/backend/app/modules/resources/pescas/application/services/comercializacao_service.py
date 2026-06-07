from __future__ import annotations

from datetime import date
from decimal import Decimal
from uuid import UUID

from apps.backend.app.modules.resources.pescas.domain.models.comercializacao_pesca import (
    ComercializacaoPesca,
)


class ComercializacaoService:
    def __init__(self) -> None:
        self._items: dict[UUID, ComercializacaoPesca] = {}

    async def registrar_operacao(
        self,
        *,
        produto: str,
        quantidade_kg: Decimal,
        preco_unitario: Decimal,
        data_operacao: date,
        comprador: str,
    ) -> ComercializacaoPesca:
        item = ComercializacaoPesca.registrar(
            produto=produto,
            quantidade_kg=quantidade_kg,
            preco_unitario=preco_unitario,
            data_operacao=data_operacao,
            comprador=comprador,
        )
        self._items[item.id] = item
        return item

    async def listar(self) -> list[ComercializacaoPesca]:
        return list(self._items.values())
