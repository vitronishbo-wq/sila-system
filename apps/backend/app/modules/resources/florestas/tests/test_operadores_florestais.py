from __future__ import annotations
from uuid import UUID
import pytest
from apps.backend.app.modules.resources.florestas.application.services.operador_florestal_service import OperadorFlorestalService

class _Repo:

    def __init__(self):
        self._items = {}

    async def save(self, operador):
        self._items[operador.id] = operador
        return operador

    async def get_by_id(self, operador_id: UUID):
        return self._items.get(operador_id)

    async def get_by_nif(self, nif: str):
        return next((i for i in self._items.values() if i.nif == nif), None)

    async def list_all(self, ativo=None):
        items = list(self._items.values())
        if ativo is None:
            return items
        return [i for i in items if i.ativo is ativo]

@pytest.mark.asyncio
async def test_cadastrar_operador_sucesso():
    service = OperadorFlorestalService(repository=_Repo())
    result = await service.cadastrar_operador(nome='Empresa Verde', nif='500000001')
    assert result.nome == 'Empresa Verde'
    assert result.nif == '500000001'