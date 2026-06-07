from __future__ import annotations

from datetime import date

from apps.backend.app.modules.resources.agricultura.application.services.insumo_service import (
    InsumoService,
)
from apps.backend.app.modules.resources.agricultura.domain.enums import StatusEstoque
from apps.backend.app.modules.resources.agricultura.domain.models.estoque import Estoque
from apps.backend.app.modules.resources.agricultura.exceptions import EstoqueNotFoundError


class EstoqueService:
    def __init__(self, *, insumo_service: InsumoService) -> None:
        self._insumo_service = insumo_service
        self._items: dict[str, Estoque] = {}
        self._seq = 0

    def _next_codigo(self) -> str:
        self._seq += 1
        return f"EST/{date.today().year}/{self._seq:06d}"

    async def criar_controle(self, *, codigo_insumo: str, quantidade_minima: float) -> Estoque:
        insumo = await self._insumo_service.obter(codigo_insumo)
        item = Estoque.criar(
            codigo_insumo=codigo_insumo,
            quantidade_atual=insumo.quantidade_estoque,
            quantidade_minima=quantidade_minima,
        )
        item.codigo_estoque = self._next_codigo()
        self._items[item.codigo_estoque] = item
        return item

    async def obter(self, codigo_estoque: str) -> Estoque:
        item = self._items.get(codigo_estoque)
        if not item:
            raise EstoqueNotFoundError("Controle de estoque nao encontrado")
        insumo = await self._insumo_service.obter(item.codigo_insumo)
        item.atualizar_quantidade(insumo.quantidade_estoque)
        return item

    async def listar(self, *, somente_baixo: bool = False) -> list[Estoque]:
        result: list[Estoque] = []
        for codigo in list(self._items.keys()):
            item = await self.obter(codigo)
            if somente_baixo and item.status == StatusEstoque.NORMAL:
                continue
            result.append(item)
        return result
