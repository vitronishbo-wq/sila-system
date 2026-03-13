from __future__ import annotations
from decimal import Decimal
from uuid import UUID, uuid4
import pytest
from app.modules.resources.florestas.application.services.inventario_service import InventarioService

class _Repo:

    def __init__(self):
        self._items = {}

    async def save(self, inventario):
        self._items[inventario.id] = inventario
        return inventario

    async def get_by_id(self, inventario_id: UUID):
        return self._items.get(inventario_id)

    async def list_by_unidade(self, unidade_manejo_id: UUID):
        return [i for i in self._items.values() if i.unidade_manejo_id == unidade_manejo_id]

@pytest.mark.asyncio
async def test_registrar_inventario_sucesso():
    service = InventarioService(inventario_repo=_Repo())
    unidade_id = uuid4()
    result = await service.registrar_inventario(unidade_manejo_id=unidade_id, volume_estimado_m3=Decimal('300.50'), area_inventariada_ha=Decimal('25.0'))
    assert result.unidade_manejo_id == unidade_id