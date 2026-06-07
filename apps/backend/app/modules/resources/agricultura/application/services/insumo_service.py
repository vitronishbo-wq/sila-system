from __future__ import annotations

from datetime import date

from apps.backend.app.modules.resources.agricultura.domain.models.insumo import Insumo
from apps.backend.app.modules.resources.agricultura.exceptions import InsumoNotFoundError


class InsumoService:
    def __init__(self) -> None:
        self._items: dict[str, Insumo] = {}
        self._seq = 0

    def _next_codigo(self) -> str:
        self._seq += 1
        return f"INS/{date.today().year}/{self._seq:06d}"

    async def cadastrar(
        self,
        *,
        nome: str,
        tipo,
        unidade_medida: str,
        quantidade_inicial: float,
        custo_unitario: float,
    ) -> Insumo:
        item = Insumo.criar(
            nome=nome,
            tipo=tipo,
            unidade_medida=unidade_medida,
            quantidade_inicial=quantidade_inicial,
            custo_unitario=custo_unitario,
        )
        item.codigo_insumo = self._next_codigo()
        self._items[item.codigo_insumo] = item
        return item

    async def registrar_entrada(self, codigo_insumo: str, quantidade: float) -> Insumo:
        item = self._items.get(codigo_insumo)
        if not item:
            raise InsumoNotFoundError("Insumo nao encontrado")
        item.registrar_entrada(quantidade)
        return item

    async def registrar_baixa(self, codigo_insumo: str, quantidade: float) -> Insumo:
        item = self._items.get(codigo_insumo)
        if not item:
            raise InsumoNotFoundError("Insumo nao encontrado")
        item.registrar_baixa(quantidade)
        return item

    async def obter(self, codigo_insumo: str) -> Insumo:
        item = self._items.get(codigo_insumo)
        if not item:
            raise InsumoNotFoundError("Insumo nao encontrado")
        return item

    async def listar(self) -> list[Insumo]:
        return list(self._items.values())
