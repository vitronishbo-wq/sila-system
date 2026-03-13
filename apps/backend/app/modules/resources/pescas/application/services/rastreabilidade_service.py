from __future__ import annotations
from uuid import UUID
from apps.backend.app.modules.resources.pescas.domain.models.rastreabilidade_pesca import RastreabilidadePesca

class RastreabilidadeService:

    def __init__(self) -> None:
        self._items: dict[UUID, RastreabilidadePesca] = {}

    async def registrar_evento(self, *, lote_codigo: str, origem_captura_id: UUID, etapa: str, operador: str) -> RastreabilidadePesca:
        item = RastreabilidadePesca.registrar(lote_codigo=lote_codigo, origem_captura_id=origem_captura_id, etapa=etapa, operador=operador)
        self._items[item.id] = item
        return item

    async def listar(self) -> list[RastreabilidadePesca]:
        return list(self._items.values())