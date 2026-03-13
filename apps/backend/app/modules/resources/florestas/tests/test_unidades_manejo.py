from __future__ import annotations
from decimal import Decimal
from uuid import UUID, uuid4
import pytest
from apps.backend.app.modules.resources.florestas.application.services.manejo_service import ManejoService
from apps.backend.app.modules.resources.florestas.domain.enums import TipoCicloCorte, TipoManejo

class _Repo:

    def __init__(self):
        self._items = {}

    async def save(self, unidade):
        self._items[unidade.id] = unidade
        return unidade

    async def get_by_id(self, unidade_id: UUID):
        return self._items.get(unidade_id)

    async def get_by_codigo(self, codigo_um: str):
        return next((i for i in self._items.values() if i.codigo_um == codigo_um), None)

    async def list_by_operador(self, operador_id: UUID):
        return [i for i in self._items.values() if i.operador_id == operador_id]

    async def list_by_tipo(self, tipo_manejo: TipoManejo):
        return [i for i in self._items.values() if i.tipo_manejo == tipo_manejo]

    async def next_codigo(self, operador_id: UUID):
        return f'UM/{operador_id}/2026/0001'

@pytest.mark.asyncio
async def test_cadastrar_unidade_sucesso():
    repo = _Repo()
    service = ManejoService(unidade_repo=repo)
    operador_id = uuid4()
    result = await service.cadastrar_unidade(nome='UM Floresta Sul', area_total_ha=Decimal('500.00'), tipo_manejo=TipoManejo.SUSTENTAVEL, ciclo_corte=TipoCicloCorte.DECENAL, operador_id=operador_id, imovel_id=uuid4())
    assert result.codigo_um.endswith('0001')
    assert result.area_manejo_ha == Decimal('400.000')