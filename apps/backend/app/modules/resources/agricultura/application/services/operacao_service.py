from __future__ import annotations
from datetime import date
from app.modules.resources.agricultura.application.services.insumo_service import InsumoService
from app.modules.resources.agricultura.application.services.safra_service import SafraService
from app.modules.resources.agricultura.domain.models.operacao import Operacao
from app.modules.resources.agricultura.exceptions import OperacaoNotFoundError

class OperacaoService:

    def __init__(self, *, safra_service: SafraService, insumo_service: InsumoService) -> None:
        self._safra_service = safra_service
        self._insumo_service = insumo_service
        self._items: dict[str, Operacao] = {}
        self._seq = 0

    def _next_codigo(self) -> str:
        self._seq += 1
        return f'OPE/{date.today().year}/{self._seq:06d}'

    async def registrar_operacao(self, *, codigo_safra: str, tipo, descricao: str, codigo_insumo: str | None=None, quantidade_insumo: float | None=None) -> Operacao:
        await self._safra_service.obter(codigo_safra)
        if codigo_insumo:
            await self._insumo_service.registrar_baixa(codigo_insumo, quantidade_insumo or 0)
        item = Operacao.registrar(codigo_safra=codigo_safra, tipo=tipo, descricao=descricao, codigo_insumo=codigo_insumo, quantidade_insumo=quantidade_insumo)
        item.codigo_operacao = self._next_codigo()
        self._items[item.codigo_operacao] = item
        return item

    async def obter(self, codigo_operacao: str) -> Operacao:
        item = self._items.get(codigo_operacao)
        if not item:
            raise OperacaoNotFoundError('Operacao nao encontrada')
        return item

    async def listar(self, *, codigo_safra: str | None=None) -> list[Operacao]:
        values = list(self._items.values())
        if codigo_safra:
            values = [item for item in values if item.codigo_safra == codigo_safra]
        return values