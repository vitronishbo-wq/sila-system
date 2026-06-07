from __future__ import annotations

from datetime import date

from apps.backend.app.modules.resources.agricultura.application.services.safra_service import (
    SafraService,
)
from apps.backend.app.modules.resources.agricultura.domain.enums import StatusSafra
from apps.backend.app.modules.resources.agricultura.domain.models.comercializacao import (
    Comercializacao,
)
from apps.backend.app.modules.resources.agricultura.exceptions import ComercializacaoNotFoundError


class ComercializacaoService:
    def __init__(self, *, safra_service: SafraService) -> None:
        self._safra_service = safra_service
        self._items: dict[str, Comercializacao] = {}
        self._seq = 0

    def _next_codigo(self) -> str:
        self._seq += 1
        return f"COM/{date.today().year}/{self._seq:06d}"

    async def registrar_venda(
        self, *, codigo_safra: str, comprador: str, quantidade_ton: float, preco_unitario: float
    ) -> Comercializacao:
        safra = await self._safra_service.obter(codigo_safra)
        if safra.status != StatusSafra.COLHIDA:
            raise ValueError("Somente safras colhidas podem ser comercializadas")
        if safra.producao_real_ton is not None and quantidade_ton > safra.producao_real_ton:
            raise ValueError("Quantidade vendida nao pode exceder producao real da safra")
        item = Comercializacao.registrar(
            codigo_safra=codigo_safra,
            comprador=comprador,
            quantidade_ton=quantidade_ton,
            preco_unitario=preco_unitario,
        )
        item.codigo_comercializacao = self._next_codigo()
        self._items[item.codigo_comercializacao] = item
        return item

    async def obter(self, codigo_comercializacao: str) -> Comercializacao:
        item = self._items.get(codigo_comercializacao)
        if not item:
            raise ComercializacaoNotFoundError("Comercializacao nao encontrada")
        return item

    async def listar(self, *, codigo_safra: str | None = None) -> list[Comercializacao]:
        values = list(self._items.values())
        if codigo_safra:
            values = [item for item in values if item.codigo_safra == codigo_safra]
        return values
