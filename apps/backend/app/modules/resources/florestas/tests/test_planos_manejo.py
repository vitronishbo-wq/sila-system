from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4
import pytest
from apps.backend.app.modules.resources.florestas.application.services.plano_manejo_service import PlanoManejoService
from apps.backend.app.modules.resources.florestas.domain.enums import TipoCicloCorte, TipoManejo
from apps.backend.app.modules.resources.florestas.domain.models.unidade_manejo import UnidadeManejo

class _PlanoRepo:

    def __init__(self):
        self._items = {}

    async def save(self, plano):
        self._items[plano.id] = plano
        return plano

    async def get_by_id(self, plano_id: UUID):
        return self._items.get(plano_id)

    async def get_by_numero(self, numero_pmfs: str):
        return next((i for i in self._items.values() if i.numero_pmfs == numero_pmfs), None)

    async def list_by_unidade(self, unidade_manejo_id: UUID):
        return [i for i in self._items.values() if i.unidade_manejo_id == unidade_manejo_id]

class _UnidadeRepo:

    def __init__(self, unidade: UnidadeManejo):
        self.unidade = unidade

    async def get_by_id(self, unidade_id: UUID):
        return self.unidade if self.unidade.id == unidade_id else None

@pytest.mark.asyncio
async def test_submeter_plano_sucesso():
    unidade = UnidadeManejo(id=uuid4(), codigo_um='UM/ABC/2026/0001', nome='UM Norte', area_total_ha=Decimal('100.0'), area_manejo_ha=Decimal('80.0'), area_preservacao_ha=Decimal('20.0'), tipo_manejo=TipoManejo.SUSTENTAVEL, ciclo_corte=TipoCicloCorte.DECENAL, operador_id=uuid4(), imovel_id=uuid4(), data_criacao=date.today())
    service = PlanoManejoService(plano_repo=_PlanoRepo(), unidade_repo=_UnidadeRepo(unidade))
    plano = await service.submeter_plano(unidade_manejo_id=unidade.id, responsavel_tecnico_id=uuid4(), responsavel_tecnico_registro='ENG-123', volume_anual_estimado_m3=Decimal('1500'), ciclo_corte_anos=10, area_anual_ha=Decimal('50'))
    assert plano.numero_pmfs.startswith('PMFS-')