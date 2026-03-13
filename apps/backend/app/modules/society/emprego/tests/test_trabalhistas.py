from __future__ import annotations
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.modules.society.emprego.api.deps import get_trabalho_service
from app.modules.society.emprego.api.endpoints.trabalhistas import router as trabalhistas_router
from app.modules.society.emprego.application.services.trabalho_service import TrabalhoService

@pytest.mark.asyncio
async def test_criar_registro_trabalhista_rejeita_cidadao_inativo():
    repository = SimpleNamespace(exists_active_for_citizen=AsyncMock(return_value=False), next_numero_processo=AsyncMock(), save=AsyncMock())
    citizen_service = SimpleNamespace(is_citizen_active=AsyncMock(return_value=False))
    service = TrabalhoService(repository=repository, citizen_service=citizen_service)
    with pytest.raises(ValueError, match='nao encontrado ou inativo'):
        await service.criar_registro(service_type='reclamacao_trabalhista', citizen_id=uuid4(), observacoes='Queixa formal', metadata={'origem': 'portal'})
    repository.next_numero_processo.assert_not_awaited()

def _build_client(service) -> TestClient:
    app = FastAPI()
    app.include_router(trabalhistas_router, prefix='/emprego')
    app.dependency_overrides[get_trabalho_service] = lambda: service
    return TestClient(app)

def test_endpoint_criar_trabalhista_retorna_400_para_regra_negocio():
    service = SimpleNamespace(criar_registro=AsyncMock(side_effect=ValueError('Regra invalida')))
    client = _build_client(service)
    response = client.post('/emprego/trabalho/reclamacoes', json={'citizen_id': str(uuid4()), 'metadata': {'origem': 'portal'}})
    assert response.status_code == 400
    assert 'regra invalida' in response.json()['detail'].lower()