from __future__ import annotations
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch
from uuid import uuid4
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.api.deps import get_current_user
from app.modules.justice.bounded_contexts.api.citizens.citizens_routes import get_citizen_service, router as citizens_router

def _build_client(service) -> TestClient:
    app = FastAPI()
    app.include_router(citizens_router, prefix='/identidade-civil')
    app.dependency_overrides[get_current_user] = lambda: SimpleNamespace(id=uuid4())
    app.dependency_overrides[get_citizen_service] = lambda: service
    return TestClient(app)

def test_endpoint_get_citizen_completo_retorna_200() -> None:
    citizen_id = str(uuid4())
    payload = {'cidadao': {'id': citizen_id, 'full_name': 'Joao Silva'}, 'integracoes': {'educacao': {'tem_matricula_ativa': True}}}
    service = SimpleNamespace(get_citizen_completo=AsyncMock(return_value=payload))
    client = _build_client(service)
    response = client.get(f'/identidade-civil/citizens/{citizen_id}/completo')
    assert response.status_code == 200
    assert response.json()['cidadao']['id'] == citizen_id

def test_endpoint_get_citizen_completo_retorna_404() -> None:
    service = SimpleNamespace(get_citizen_completo=AsyncMock(return_value=None))
    client = _build_client(service)
    response = client.get(f'/identidade-civil/citizens/{uuid4()}/completo')
    assert response.status_code == 404
    assert 'não encontrado' in response.json()['detail'].lower()

def test_provider_get_citizen_service_faz_wiring_completo() -> None:
    fake_db = object()
    with patch('app.modules.justice.bounded_contexts.api.citizens.citizens_routes.SQLAlchemyMatriculaRepository', return_value='repo_educacao'), patch('app.modules.justice.bounded_contexts.api.citizens.citizens_routes.SQLAlchemyJovemRepository', return_value='repo_juventude'), patch('app.modules.justice.bounded_contexts.api.citizens.citizens_routes.SQLAlchemyCandidatoRepository', return_value='repo_emprego'), patch('app.modules.justice.bounded_contexts.api.citizens.citizens_routes.MedicalRecordRepository', return_value='repo_saude'), patch('app.modules.justice.bounded_contexts.api.citizens.citizens_routes.SQLAlchemyBeneficiarioRepository', return_value='repo_assistencia'), patch('app.modules.justice.bounded_contexts.api.citizens.citizens_routes.EducacaoServiceAdapter', return_value='adapter_educacao'), patch('app.modules.justice.bounded_contexts.api.citizens.citizens_routes.JuventudeServiceAdapter', return_value='adapter_juventude'), patch('app.modules.justice.bounded_contexts.api.citizens.citizens_routes.EmpregoServiceAdapter', return_value='adapter_emprego'), patch('app.modules.justice.bounded_contexts.api.citizens.citizens_routes.SaudeServiceAdapter', return_value='adapter_saude'), patch('app.modules.justice.bounded_contexts.api.citizens.citizens_routes.AssistenciaSocialServiceAdapter', return_value='adapter_assistencia'), patch('app.modules.justice.bounded_contexts.api.citizens.citizens_routes.CitizenService', return_value='citizen_service') as citizen_service_cls:
        service = get_citizen_service(db=fake_db)
    assert service == 'citizen_service'
    citizen_service_cls.assert_called_once_with(educacao_service='adapter_educacao', juventude_service='adapter_juventude', emprego_service='adapter_emprego', saude_service='adapter_saude', assistencia_social_service='adapter_assistencia')