from __future__ import annotations
from datetime import date
from uuid import UUID
from app.modules.resources.pecuaria.domain.models.producao_carne import ProducaoCarne
from app.modules.resources.pecuaria.domain.models.producao_leite import ProducaoLeite

class ProducaoService:

    def __init__(self) -> None:
        self._leite: dict[UUID, ProducaoLeite] = {}
        self._carne: dict[UUID, ProducaoCarne] = {}

    async def registrar_leite(self, *, propriedade_id: UUID, litros: float, data_producao: date) -> ProducaoLeite:
        item = ProducaoLeite.registrar(propriedade_id=propriedade_id, litros=litros, data_producao=data_producao)
        self._leite[item.id] = item
        return item

    async def registrar_carne(self, *, propriedade_id: UUID, quilos: float, data_producao: date) -> ProducaoCarne:
        item = ProducaoCarne.registrar(propriedade_id=propriedade_id, quilos=quilos, data_producao=data_producao)
        self._carne[item.id] = item
        return item

    async def listar(self, propriedade_id: UUID | None=None) -> list[ProducaoLeite | ProducaoCarne]:
        items: list[ProducaoLeite | ProducaoCarne] = list(self._leite.values()) + list(self._carne.values())
        if propriedade_id:
            items = [item for item in items if item.propriedade_id == propriedade_id]
        return items