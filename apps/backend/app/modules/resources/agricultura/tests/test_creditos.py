from __future__ import annotations
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.modules.resources.agricultura.api.deps import get_credito_service
from app.modules.resources.agricultura.api.endpoints.creditos import router as creditos_router
from app.modules.resources.agricultura.application.services.credito_service import CreditoService
from app.modules.resources.agricultura.domain.enums import StatusCredito
from app.modules.resources.agricultura.exceptions import CreditoNotFoundError

@pytest.mark.asyncio
async def test_credito_service_fluxo_aprovar_desembolsar():
    service = CreditoService()
    credito = await service.solicitar(codigo_produtor='PRD/2026/000001', finalidade='Aquisicao de fertilizante', valor_solicitado=50000)
    assert credito.status == StatusCredito.SOLICITADO
    credito = await service.aprovar(credito.codigo_credito, valor_aprovado=45000)
    assert credito.status == StatusCredito.APROVADO
    assert credito.valor_aprovado == 45000
    credito = await service.desembolsar(credito.codigo_credito)
    assert credito.status == StatusCredito.DESEMBOLSADO

def test_endpoint_solicitar_credito_retorna_201():
    mock_item = SimpleNamespace(id=uuid4(), codigo_credito='CRD/2026/000001', codigo_produtor='PRD/2026/000001', finalidade='Aquisicao de fertilizante', valor_solicitado=50000.0, valor_aprovado=None, status='solicitado', data_solicitacao='2026-02-28', data_aprovacao=None, data_desembolso=None)
    service = SimpleNamespace(solicitar=AsyncMock(return_value=mock_item))
    app = FastAPI()
    app.include_router(creditos_router, prefix='/agricultura')
    app.dependency_overrides[get_credito_service] = lambda: service
    client = TestClient(app)
    response = client.post('/agricultura/creditos/', json={'codigo_produtor': 'PRD/2026/000001', 'finalidade': 'Aquisicao de fertilizante', 'valor_solicitado': 50000})
    assert response.status_code == 201
    assert response.json()['codigo_credito'] == 'CRD/2026/000001'

def test_endpoint_obter_credito_retorna_404():
    service = SimpleNamespace(obter=AsyncMock(side_effect=CreditoNotFoundError('Credito rural nao encontrado')))
    app = FastAPI()
    app.include_router(creditos_router, prefix='/agricultura')
    app.dependency_overrides[get_credito_service] = lambda: service
    client = TestClient(app)
    response = client.get('/agricultura/creditos/CRD/2026/999999')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Credito rural nao encontrado'