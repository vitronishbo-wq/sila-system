from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from apps.backend.app.modules.resources.pescas.domain.models.quota import Quota

class QuotaService:

    def __init__(self) -> None:
        self._items: dict[UUID, Quota] = {}

    async def criar_quota(self, *, especie_id: UUID, zona_pesca_id: UUID, limite_kg: Decimal) -> Quota:
        item = Quota.criar(especie_id=especie_id, zona_pesca_id=zona_pesca_id, ano=date.today().year, limite_kg=limite_kg)
        self._items[item.id] = item
        return item

    async def registrar_consumo(self, *, quota_id: UUID, quantidade_kg: Decimal) -> Quota:
        item = self._items.get(quota_id)
        if not item:
            raise ValueError('Quota nao encontrada')
        item.registrar_consumo(quantidade_kg)
        return item

    async def listar(self) -> list[Quota]:
        return list(self._items.values())