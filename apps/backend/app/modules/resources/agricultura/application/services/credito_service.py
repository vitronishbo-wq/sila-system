from __future__ import annotations
from datetime import date
from apps.backend.app.modules.resources.agricultura.domain.models.credito_rural import CreditoRural
from apps.backend.app.modules.resources.agricultura.exceptions import CreditoNotFoundError

class CreditoService:

    def __init__(self) -> None:
        self._items: dict[str, CreditoRural] = {}
        self._seq = 0

    def _next_codigo(self) -> str:
        self._seq += 1
        return f'CRD/{date.today().year}/{self._seq:06d}'

    async def solicitar(self, *, codigo_produtor: str, finalidade: str, valor_solicitado: float) -> CreditoRural:
        item = CreditoRural.solicitar(codigo_produtor=codigo_produtor, finalidade=finalidade, valor_solicitado=valor_solicitado)
        item.codigo_credito = self._next_codigo()
        self._items[item.codigo_credito] = item
        return item

    async def aprovar(self, codigo_credito: str, *, valor_aprovado: float) -> CreditoRural:
        item = self._items.get(codigo_credito)
        if not item:
            raise CreditoNotFoundError('Credito rural nao encontrado')
        item.aprovar(valor_aprovado)
        return item

    async def desembolsar(self, codigo_credito: str) -> CreditoRural:
        item = self._items.get(codigo_credito)
        if not item:
            raise CreditoNotFoundError('Credito rural nao encontrado')
        item.desembolsar()
        return item

    async def obter(self, codigo_credito: str) -> CreditoRural:
        item = self._items.get(codigo_credito)
        if not item:
            raise CreditoNotFoundError('Credito rural nao encontrado')
        return item

    async def listar(self, *, codigo_produtor: str | None=None) -> list[CreditoRural]:
        values = list(self._items.values())
        if codigo_produtor:
            values = [item for item in values if item.codigo_produtor == codigo_produtor]
        return values