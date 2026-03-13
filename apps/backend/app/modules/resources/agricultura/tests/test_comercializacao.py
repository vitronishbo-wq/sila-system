from __future__ import annotations
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from apps.backend.app.modules.resources.agricultura.api.deps import get_comercializacao_service
from apps.backend.app.modules.resources.agricultura.api.endpoints.comercializacao import router as comercializacao_router
from apps.backend.app.modules.resources.agricultura.application.services.comercializacao_service import ComercializacaoService
from apps.backend.app.modules.resources.agricultura.application.services.producao_service import ProducaoService
from apps.backend.app.modules.resources.agricultura.application.services.propriedade_service import PropriedadeService
from apps.backend.app.modules.resources.agricultura.application.services.safra_service import SafraService
from apps.backend.app.modules.resources.agricultura.domain.enums import StatusSafra, TipoCultura, TipoPropriedade
from apps.backend.app.modules.resources.agricultura.exceptions import ComercializacaoNotFoundError

@pytest.mark.asyncio
async def test_comercializacao_service_registrar_venda():
    propriedade_service = PropriedadeService()
    producao_service = ProducaoService()
    safra_service = SafraService(propriedade_service=propriedade_service, producao_service=producao_service)
    prop = await propriedade_service.cadastrar(produtor_id=uuid4(), nome='Fazenda Leste', tipo=TipoPropriedade.PROPRIO, area_total_ha=80, area_cultivavel_ha=65)
    cultura = await producao_service.cadastrar_cultura(nome='Milho', tipo=TipoCultura.GRAOS, ciclo_dias=120, produtividade_estimada_ton_ha=3)
    safra = await safra_service.criar_safra(codigo_propriedade=prop.codigo_propriedade, codigo_cultura=cultura.codigo_cultura, ano=2026, area_plantada_ha=30, producao_estimada_ton=90)
    await safra_service.iniciar(safra.codigo_safra)
    safra = await safra_service.colher(safra.codigo_safra, producao_real_ton=85)
    assert safra.status == StatusSafra.COLHIDA
    service = ComercializacaoService(safra_service=safra_service)
    venda = await service.registrar_venda(codigo_safra=safra.codigo_safra, comprador='Mercado Central', quantidade_ton=40, preco_unitario=1200)
    assert venda.codigo_comercializacao.startswith('COM/')
    assert venda.valor_total == 48000.0

def test_endpoint_registrar_venda_retorna_201():
    mock_item = SimpleNamespace(id=uuid4(), codigo_comercializacao='COM/2026/000001', codigo_safra='SAF/2026/000001', comprador='Mercado Central', quantidade_ton=40.0, preco_unitario=1200.0, valor_total=48000.0, data_venda='2026-02-28')
    service = SimpleNamespace(registrar_venda=AsyncMock(return_value=mock_item))
    app = FastAPI()
    app.include_router(comercializacao_router, prefix='/agricultura')
    app.dependency_overrides[get_comercializacao_service] = lambda: service
    client = TestClient(app)
    response = client.post('/agricultura/comercializacao/', json={'codigo_safra': 'SAF/2026/000001', 'comprador': 'Mercado Central', 'quantidade_ton': 40, 'preco_unitario': 1200})
    assert response.status_code == 201
    assert response.json()['codigo_comercializacao'] == 'COM/2026/000001'

def test_endpoint_obter_venda_retorna_404():
    service = SimpleNamespace(obter=AsyncMock(side_effect=ComercializacaoNotFoundError('Comercializacao nao encontrada')))
    app = FastAPI()
    app.include_router(comercializacao_router, prefix='/agricultura')
    app.dependency_overrides[get_comercializacao_service] = lambda: service
    client = TestClient(app)
    response = client.get('/agricultura/comercializacao/COM/2026/999999')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Comercializacao nao encontrada'