from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from apps.backend.app.modules.resources.pescas.domain.models.producao_pesca import ProducaoPesca

class ProducaoPescaService:

    def __init__(self) -> None:
        self._items: dict[UUID, ProducaoPesca] = {}

    async def registrar_producao(self, *, data_producao: date, quantidade_kg: Decimal, unidade_processamento: str, destino: str) -> ProducaoPesca:
        item = ProducaoPesca.registrar(data_producao=data_producao, quantidade_kg=quantidade_kg, unidade_processamento=unidade_processamento, destino=destino)
        self._items[item.id] = item
        return item

    async def listar(self) -> list[ProducaoPesca]:
        return list(self._items.values())