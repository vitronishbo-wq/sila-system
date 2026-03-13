from __future__ import annotations
from datetime import date
from uuid import UUID
from apps.backend.app.modules.resources.pescas.domain.enums import PeriodoDefesoTipo
from apps.backend.app.modules.resources.pescas.domain.models.defeso import Defeso

class DefesoService:

    def __init__(self) -> None:
        self._items: dict[UUID, Defeso] = {}

    async def criar_defeso(self, *, periodo: PeriodoDefesoTipo, especie_id: UUID, data_inicio: date, data_fim: date) -> Defeso:
        item = Defeso.criar(periodo=periodo, especie_id=especie_id, data_inicio=data_inicio, data_fim=data_fim)
        self._items[item.id] = item
        return item

    async def listar_defesos(self) -> list[Defeso]:
        return list(self._items.values())