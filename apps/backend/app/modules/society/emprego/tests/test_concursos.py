from __future__ import annotations
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.modules.society.emprego.api.deps import get_concurso_service
from app.modules.society.emprego.api.endpoints.concursos import router as concursos_router
from app.modules.society.emprego.application.services.concurso_service import ConcursoService

@pytest.mark.asyncio
async def test_criar_concurso_bloqueia_duplicidade_ativa():
    repository = SimpleNamespace(exists_active_for_citizen=AsyncMock(return_value=True), next_numero_processo=AsyncMock(), save=AsyncMock())
    citizen_service = SimpleNamespace(is_citizen_active=AsyncMock(return_value=True))
    service = ConcursoService(repository=repository, citizen_service=citizen_service)
    with pytest.raises(ValueError, match='registro ativo'):
        await service.criar_registro(service_type='concurso_publico', citizen_id=uuid4(), metadata={'concurso': 'tecnico superior'})
    repository.next_numero_processo.assert_not_awaited()

def _build_client(service) -> TestClient:
    app = FastAPI()
    app.include_router(concursos_router, prefix='/emprego')
    app.dependency_overrides[get_concurso_service] = lambda: service
    return TestClient(app)

def test_endpoint_obter_concurso_retorna_404_quando_inexistente():
    service = SimpleNamespace(obter_por_id=AsyncMock(return_value=None))
    client = _build_client(service)
    response = client.get(f'/emprego/workflow/{uuid4()}')
    assert response.status_code == 404
    assert 'nao encontrado' in response.json()['detail'].lower()