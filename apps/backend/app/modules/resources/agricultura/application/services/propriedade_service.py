from __future__ import annotations
from datetime import date
from uuid import UUID
from app.modules.resources.agricultura.domain.models.propriedade_rural import PropriedadeRural
from app.modules.resources.agricultura.exceptions import PropriedadeNotFoundError

class PropriedadeService:

    def __init__(self) -> None:
        self._items: dict[str, PropriedadeRural] = {}
        self._seq = 0

    def _next_codigo(self) -> str:
        self._seq += 1
        return f'PROP/{date.today().year}/{self._seq:06d}'

    async def cadastrar(self, *, produtor_id: UUID, nome: str, tipo, area_total_ha: float, area_cultivavel_ha: float, provincia: str | None=None, municipio: str | None=None) -> PropriedadeRural:
        item = PropriedadeRural.criar(produtor_id=produtor_id, nome=nome, tipo=tipo, area_total_ha=area_total_ha, area_cultivavel_ha=area_cultivavel_ha, provincia=provincia, municipio=municipio)
        item.codigo_propriedade = self._next_codigo()
        self._items[item.codigo_propriedade] = item
        return item

    async def obter(self, codigo_propriedade: str) -> PropriedadeRural:
        item = self._items.get(codigo_propriedade)
        if not item:
            raise PropriedadeNotFoundError('Propriedade nao encontrada')
        return item

    async def listar(self, produtor_id: UUID | None=None) -> list[PropriedadeRural]:
        values = list(self._items.values())
        if produtor_id:
            values = [item for item in values if item.produtor_id == produtor_id]
        return values