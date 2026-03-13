from __future__ import annotations
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.modules.resources.agricultura.api.deps import get_colheita_service
from app.modules.resources.agricultura.api.endpoints.colheitas import router as colheitas_router
from app.modules.resources.agricultura.application.services.colheita_service import ColheitaService
from app.modules.resources.agricultura.application.services.producao_service import ProducaoService
from app.modules.resources.agricultura.application.services.propriedade_service import PropriedadeService
from app.modules.resources.agricultura.application.services.safra_service import SafraService
from app.modules.resources.agricultura.application.services.talhao_service import TalhaoService
from app.modules.resources.agricultura.domain.enums import TipoCultura, TipoPropriedade
from app.modules.resources.agricultura.exceptions import ColheitaNotFoundError

@pytest.mark.asyncio
async def test_colheita_service_registrar():
    propriedade_service = PropriedadeService()
    producao_service = ProducaoService()
    safra_service = SafraService(propriedade_service=propriedade_service, producao_service=producao_service)
    talhao_service = TalhaoService(propriedade_service=propriedade_service)
    prop = await propriedade_service.cadastrar(produtor_id=uuid4(), nome='Fazenda Colheita', tipo=TipoPropriedade.PROPRIO, area_total_ha=70, area_cultivavel_ha=52)
    talhao = await talhao_service.cadastrar(codigo_propriedade=prop.codigo_propriedade, nome='Talhao C', area_ha=14)
    cultura = await producao_service.cadastrar_cultura(nome='Milho', tipo=TipoCultura.GRAOS, ciclo_dias=110, produtividade_estimada_ton_ha=3.2)
    safra = await safra_service.criar_safra(codigo_propriedade=prop.codigo_propriedade, codigo_cultura=cultura.codigo_cultura, ano=2026, area_plantada_ha=14, producao_estimada_ton=40)
    await safra_service.iniciar(safra.codigo_safra)
    service = ColheitaService(safra_service=safra_service, talhao_service=talhao_service)
    colheita = await service.registrar(codigo_safra=safra.codigo_safra, codigo_talhao=talhao.codigo_talhao, quantidade_colhida_ton=18, perdas_ton=1.5)
    assert colheita.codigo_colheita.startswith('COL/')
    assert colheita.quantidade_liquida_ton == 16.5

def test_endpoint_registrar_colheita_retorna_201():
    mock_item = SimpleNamespace(id=uuid4(), codigo_colheita='COL/2026/000001', codigo_safra='SAF/2026/000001', codigo_talhao='TAL/2026/000001', quantidade_colhida_ton=18.0, perdas_ton=1.5, quantidade_liquida_ton=16.5, data_colheita='2026-02-28', umidade_percentual=None, observacoes=None)
    service = SimpleNamespace(registrar=AsyncMock(return_value=mock_item))
    app = FastAPI()
    app.include_router(colheitas_router, prefix='/agricultura')
    app.dependency_overrides[get_colheita_service] = lambda: service
    client = TestClient(app)
    response = client.post('/agricultura/colheitas/', json={'codigo_safra': 'SAF/2026/000001', 'codigo_talhao': 'TAL/2026/000001', 'quantidade_colhida_ton': 18, 'perdas_ton': 1.5})
    assert response.status_code == 201
    assert response.json()['codigo_colheita'] == 'COL/2026/000001'

def test_endpoint_obter_colheita_retorna_404():
    service = SimpleNamespace(obter=AsyncMock(side_effect=ColheitaNotFoundError('Colheita nao encontrada')))
    app = FastAPI()
    app.include_router(colheitas_router, prefix='/agricultura')
    app.dependency_overrides[get_colheita_service] = lambda: service
    client = TestClient(app)
    response = client.get('/agricultura/colheitas/COL/2026/999999')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Colheita nao encontrada'