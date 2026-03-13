from __future__ import annotations
from datetime import date
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from apps.backend.app.modules.economy.trade.external.api.deps import get_drawback_integrado_service
from apps.backend.app.modules.economy.trade.external.api.endpoints.drawback_integrado import router as drawback_integrado_router
from apps.backend.app.modules.economy.trade.external.application.services import DrawbackIntegradoService
from apps.backend.app.modules.economy.trade.external.domain.enums import StatusHabilitacao, TipoPessoa
from apps.backend.app.modules.economy.trade.external.exceptions import DrawbackIntegradoAlreadyExistsError, DrawbackIntegradoNotFoundError
from apps.backend.app.modules.economy.trade.external.infrastructure.repositories import InMemoryDrawbackIntegradoRepository

@pytest.mark.asyncio
async def test_service_fluxo_principal_drawback_integrado():
    service = DrawbackIntegradoService(repository=InMemoryDrawbackIntegradoRepository())
    item = await service.solicitar(tipo_pessoa=TipoPessoa.JURIDICA, razao_social='Drawback Integrado SA', cnpj_cpf='50020030000157', numero_processo='PROC-DRAW-INT-2026-001', data_solicitacao=date(2026, 3, 15))
    assert item.status == StatusHabilitacao.PENDENTE
    item = await service.rejeitar(item.id, data_analise=date(2026, 3, 18), motivo='Pendencia documental')
    assert item.status == StatusHabilitacao.CANCELADO
    item = await service.reabrir(item.id)
    assert item.status == StatusHabilitacao.PENDENTE
    item = await service.aprovar(item.id, numero_radar='RADAR-DRAW-2026-5004', data_analise=date(2026, 3, 20), data_validade=date(2027, 3, 20))
    assert item.status == StatusHabilitacao.HABILITADO

@pytest.mark.asyncio
async def test_service_detecta_processo_duplicado_drawback_integrado():
    service = DrawbackIntegradoService(repository=InMemoryDrawbackIntegradoRepository())
    payload = dict(tipo_pessoa=TipoPessoa.JURIDICA, razao_social='Duplicada Drawback Integrado SA', cnpj_cpf='50020030000158', numero_processo='PROC-DRAW-INT-2026-002', data_solicitacao=date(2026, 3, 15))
    await service.solicitar(**payload)
    with pytest.raises(DrawbackIntegradoAlreadyExistsError):
        await service.solicitar(**payload)

def test_endpoint_solicitar_drawback_integrado_retorna_201():
    service = DrawbackIntegradoService(repository=InMemoryDrawbackIntegradoRepository())
    app = FastAPI()
    app.include_router(drawback_integrado_router, prefix='/comercio_externo')
    app.dependency_overrides[get_drawback_integrado_service] = lambda: service
    client = TestClient(app)
    response = client.post('/comercio_externo/drawback_integrado/', json={'tipo_pessoa': 'juridica', 'razao_social': 'HTTP Drawback Integrado SA', 'cnpj_cpf': '50020030000159', 'numero_processo': 'PROC-DRAW-INT-2026-003', 'data_solicitacao': '2026-03-15'})
    assert response.status_code == 201
    assert response.json()['status'] == 'pendente'

def test_endpoint_obter_drawback_integrado_retorna_404():
    service = SimpleNamespace(obter_por_id=AsyncMock(side_effect=DrawbackIntegradoNotFoundError('Drawback Integrado nao encontrado')))
    app = FastAPI()
    app.include_router(drawback_integrado_router, prefix='/comercio_externo')
    app.dependency_overrides[get_drawback_integrado_service] = lambda: service
    client = TestClient(app)
    response = client.get(f'/comercio_externo/drawback_integrado/{uuid4()}')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Drawback Integrado nao encontrado'