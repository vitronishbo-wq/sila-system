from __future__ import annotations
from datetime import date
from uuid import UUID
from apps.backend.app.modules.resources.pecuaria.domain.models.reproducao import Reproducao

class ReproducaoService:

    def __init__(self) -> None:
        self._items: dict[UUID, Reproducao] = {}

    async def registrar(self, *, femea_id: UUID, metodo: str, data_evento: date, macho_id: UUID | None=None) -> Reproducao:
        item = Reproducao.registrar(femea_id=femea_id, metodo=metodo, data_evento=data_evento, macho_id=macho_id)
        self._items[item.id] = item
        return item

    async def listar(self, femea_id: UUID | None=None) -> list[Reproducao]:
        values = list(self._items.values())
        if femea_id:
            values = [item for item in values if item.femea_id == femea_id]
        return values