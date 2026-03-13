from __future__ import annotations
from datetime import date, timedelta
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.api.deps import get_licenciamento_urbano_service
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.api.endpoints.licencas_urbanisticas import router as licencas_urbanisticas_router
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.application.services.licenciamento_urbano_service import LicenciamentoUrbanoService
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import StatusLicencaUrbanistica, TipoAlvara
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.exceptions import LicencaUrbanisticaNotFoundError
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.infrastructure.repositories import SQLAlchemyLicencaUrbanisticaRepository

@pytest.mark.asyncio
async def test_licenciamento_urbano_service_fluxo_sucesso():
    service = LicenciamentoUrbanoService(licenca_repo=SQLAlchemyLicencaUrbanisticaRepository())
    item = await service.criar(numero_processo='PROC-URB-2026-0001', tipo_alvara=TipoAlvara.CONSTRUCAO, requerente_id=uuid4(), zoneamento_id=uuid4(), provincia='Luanda', municipio='Luanda', endereco_obra='Rua da Missao, 120', area_construida_prevista=Decimal('850.50'))
    assert item.status == StatusLicencaUrbanistica.REQUERIDA
    assert item.codigo_licenca.startswith('LIC/')
    item = await service.iniciar_analise(item.codigo_licenca)
    assert item.status == StatusLicencaUrbanistica.EM_ANALISE
    item = await service.solicitar_pendencia(item.codigo_licenca, motivo='Falta ART assinada')
    assert item.status == StatusLicencaUrbanistica.PENDENTE_DOCUMENTACAO
    item = await service.iniciar_analise(item.codigo_licenca)
    assert item.status == StatusLicencaUrbanistica.EM_ANALISE
    item = await service.deferir(item.codigo_licenca, data_emissao=date.today(), data_validade=date.today() + timedelta(days=365), tecnico_responsavel_id=uuid4())
    assert item.status == StatusLicencaUrbanistica.DEFERIDA

def test_endpoint_criar_licenca_urbanistica_retorna_201():
    mock_item = SimpleNamespace(id=uuid4(), codigo_licenca='LIC/2026/000001', numero_processo='PROC-URB-2026-0001', tipo_alvara=TipoAlvara.CONSTRUCAO, status=StatusLicencaUrbanistica.REQUERIDA, requerente_id=uuid4(), zoneamento_id=uuid4(), provincia='Luanda', municipio='Luanda', endereco_obra='Rua da Missao, 120', area_construida_prevista=Decimal('850.50'), data_requerimento=date(2026, 3, 1), data_emissao=None, data_validade=None, tecnico_responsavel_id=None, observacoes=None, data_atualizacao=None)
    service = SimpleNamespace(criar=AsyncMock(return_value=mock_item))
    app = FastAPI()
    app.include_router(licencas_urbanisticas_router, prefix='/urbanismo-habitacao')
    app.dependency_overrides[get_licenciamento_urbano_service] = lambda: service
    client = TestClient(app)
    response = client.post('/urbanismo-habitacao/licencas-urbanisticas/', json={'numero_processo': 'PROC-URB-2026-0001', 'tipo_alvara': 'construcao', 'requerente_id': str(uuid4()), 'zoneamento_id': str(uuid4()), 'provincia': 'Luanda', 'municipio': 'Luanda', 'endereco_obra': 'Rua da Missao, 120', 'area_construida_prevista': '850.50'})
    assert response.status_code == 201
    assert response.json()['codigo_licenca'] == 'LIC/2026/000001'

def test_endpoint_obter_licenca_urbanistica_retorna_404():
    service = SimpleNamespace(obter_por_codigo=AsyncMock(side_effect=LicencaUrbanisticaNotFoundError('Licenca urbanistica nao encontrada')))
    app = FastAPI()
    app.include_router(licencas_urbanisticas_router, prefix='/urbanismo-habitacao')
    app.dependency_overrides[get_licenciamento_urbano_service] = lambda: service
    client = TestClient(app)
    response = client.get('/urbanismo-habitacao/licencas-urbanisticas/LIC/2026/999999')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Licenca urbanistica nao encontrada'

def test_endpoint_deferir_licenca_sem_adapter_critico_retorna_503():
    service = SimpleNamespace(deferir=AsyncMock())
    service.has_ambiente_adapter = lambda: True
    service.has_financas_adapter = lambda: False
    service.has_workflow_adapter = lambda: True
    app = FastAPI()
    app.include_router(licencas_urbanisticas_router, prefix='/urbanismo-habitacao')
    app.dependency_overrides[get_licenciamento_urbano_service] = lambda: service
    client = TestClient(app)
    response = client.post('/urbanismo-habitacao/licencas-urbanisticas/LIC/2026/000001/deferir', json={'data_emissao': '2026-03-04', 'data_validade': '2027-03-04', 'tecnico_responsavel_id': str(uuid4())})
    assert response.status_code == 503
    assert 'Financas indisponivel' in response.json()['detail']
    service.deferir.assert_not_awaited()