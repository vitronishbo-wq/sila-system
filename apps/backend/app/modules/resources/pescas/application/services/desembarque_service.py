from __future__ import annotations
from decimal import Decimal
from uuid import UUID
from app.modules.resources.pescas.domain.models.desembarque import Desembarque

class DesembarqueService:

    def __init__(self) -> None:
        self._items: dict[UUID, Desembarque] = {}

    async def registrar_desembarque(self, *, captura_id: UUID, porto_desembarque: str, quantidade_kg: Decimal) -> Desembarque:
        item = Desembarque.registrar(captura_id=captura_id, porto_desembarque=porto_desembarque, quantidade_kg=quantidade_kg)
        self._items[item.id] = item
        return item

    async def listar(self) -> list[Desembarque]:
        return list(self._items.values())