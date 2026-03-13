from __future__ import annotations
from datetime import date
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from apps.backend.app.modules.economy.trade.external.api.deps import get_exportador_service
from apps.backend.app.modules.economy.trade.external.api.endpoints.exportadores import router as exportadores_router
from apps.backend.app.modules.economy.trade.external.application.services import ExportadorService
from apps.backend.app.modules.economy.trade.external.domain.enums import RegimeExportacao, StatusHabilitacao, TipoPessoa
from apps.backend.app.modules.economy.trade.external.exceptions import ExportadorAlreadyExistsError, ExportadorNotFoundError
from apps.backend.app.modules.economy.trade.external.infrastructure.repositories import InMemoryExportadorRepository

@pytest.mark.asyncio
async def test_service_fluxo_principal_exportador():
    service = ExportadorService(repository=InMemoryExportadorRepository())
    item = await service.cadastrar(razao_social='Export Angola SA', cnpj_cpf='50020030000199', tipo_pessoa=TipoPessoa.JURIDICA, endereco='Av. Comercio Exterior', numero='100', bairro='Centro', municipio='Luanda', provincia='Luanda', cep='1000-001', regimes_autorizados=[RegimeExportacao.DEFINITIVA])
    assert item.status == StatusHabilitacao.PENDENTE
    item = await service.habilitar(item.id, numero_radar='RADAR-2026-0001', data_habilitacao=date(2026, 3, 1), data_validade=date(2027, 3, 1))
    assert item.status == StatusHabilitacao.HABILITADO
    assert item.cadastro_radar == 'RADAR-2026-0001'
    item = await service.adicionar_produto(item.id, produto='Cafe')
    item = await service.adicionar_pais_destino(item.id, pais='br')
    assert item.produtos_principais == ['Cafe']
    assert item.paises_destino == ['BR']
    item = await service.suspender(item.id, data_suspensao=date(2026, 6, 1), motivo='Auditoria documental')
    assert item.status == StatusHabilitacao.SUSPENSO
    item = await service.reabilitar(item.id)
    assert item.status == StatusHabilitacao.HABILITADO
    item = await service.cancelar(item.id, data_cancelamento=date(2026, 12, 1), motivo='Encerramento operacional')
    assert item.status == StatusHabilitacao.CANCELADO

@pytest.mark.asyncio
async def test_service_detecta_cnpj_cpf_duplicado():
    service = ExportadorService(repository=InMemoryExportadorRepository())
    payload = dict(razao_social='Duplicado Export SA', cnpj_cpf='50020030000188', tipo_pessoa=TipoPessoa.JURIDICA, endereco='Rua A', numero='1', bairro='Centro', municipio='Luanda', provincia='Luanda', cep='1000-100', regimes_autorizados=[RegimeExportacao.DEFINITIVA])
    await service.cadastrar(**payload)
    with pytest.raises(ExportadorAlreadyExistsError):
        await service.cadastrar(**payload)

def test_endpoint_cadastrar_retorna_201():
    repository = InMemoryExportadorRepository()
    service = ExportadorService(repository=repository)
    app = FastAPI()
    app.include_router(exportadores_router, prefix='/comercio_externo')
    app.dependency_overrides[get_exportador_service] = lambda: service
    client = TestClient(app)
    response = client.post('/comercio_externo/exportadores/', json={'razao_social': 'Export Teste SA', 'cnpj_cpf': '50020030000177', 'tipo_pessoa': 'juridica', 'endereco': 'Av. Marginal', 'numero': '50', 'bairro': 'Ingombota', 'municipio': 'Luanda', 'provincia': 'Luanda', 'cep': '1000-200', 'regimes_autorizados': ['definitiva', 'temporaria']})
    assert response.status_code == 201
    assert response.json()['status'] == 'pendente'

def test_endpoint_obter_por_id_retorna_404():
    service = SimpleNamespace(obter_por_id=AsyncMock(side_effect=ExportadorNotFoundError('Exportador nao encontrado')))
    app = FastAPI()
    app.include_router(exportadores_router, prefix='/comercio_externo')
    app.dependency_overrides[get_exportador_service] = lambda: service
    client = TestClient(app)
    response = client.get(f'/comercio_externo/exportadores/{uuid4()}')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Exportador nao encontrado'

def test_http_full_cycle_exportador():
    service = ExportadorService(repository=InMemoryExportadorRepository())
    app = FastAPI()
    app.include_router(exportadores_router, prefix='/comercio_externo')
    app.dependency_overrides[get_exportador_service] = lambda: service
    client = TestClient(app)
    create_resp = client.post('/comercio_externo/exportadores/', json={'razao_social': 'Export Ciclo SA', 'cnpj_cpf': '50020030000166', 'tipo_pessoa': 'juridica', 'endereco': 'Rua Porto', 'numero': '10', 'bairro': 'Portuario', 'municipio': 'Lobito', 'provincia': 'Benguela', 'cep': '2000-300', 'regimes_autorizados': ['definitiva']})
    assert create_resp.status_code == 201
    item_id = create_resp.json()['id']
    habilitar_resp = client.patch(f'/comercio_externo/exportadores/{item_id}/habilitar', json={'numero_radar': 'RADAR-2026-1000', 'data_habilitacao': '2026-03-10', 'data_validade': '2027-03-10'})
    assert habilitar_resp.status_code == 200
    assert habilitar_resp.json()['status'] == 'habilitado'
    produto_resp = client.patch(f'/comercio_externo/exportadores/{item_id}/produtos', json={'produto': 'Diamante'})
    assert produto_resp.status_code == 200
    assert produto_resp.json()['produtos_principais'] == ['Diamante']
    pais_resp = client.patch(f'/comercio_externo/exportadores/{item_id}/paises-destino', json={'pais': 'za'})
    assert pais_resp.status_code == 200
    assert pais_resp.json()['paises_destino'] == ['ZA']
    listar_resp = client.get('/comercio_externo/exportadores/')
    assert listar_resp.status_code == 200
    assert any((item['id'] == item_id for item in listar_resp.json()))