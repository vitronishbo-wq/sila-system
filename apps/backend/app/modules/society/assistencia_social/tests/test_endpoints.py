from __future__ import annotations
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
from fastapi import FastAPI
from fastapi.testclient import TestClient
from apps.backend.app.modules.society.assistencia_social.api.deps import get_beneficiario_service, get_beneficio_service, get_cadastro_unico_service
from apps.backend.app.modules.society.assistencia_social.api.router import router as assistencia_social_router
from apps.backend.app.modules.society.assistencia_social.application.services.cadastro_unico_service import CadastroUnicoService
from apps.backend.app.modules.society.assistencia_social.domain.enums import TipoBeneficio
from apps.backend.app.modules.society.assistencia_social.domain.models import Beneficio
from apps.backend.app.modules.society.assistencia_social.tests._fakes import FakeCitizenService, FakeEducacaoService, FakeJuventudeService, InMemoryCadastroUnicoRepo

def _build_client(overrides: dict) -> TestClient:
    app = FastAPI()
    app.include_router(assistencia_social_router)
    for dep, service in overrides.items():
        app.dependency_overrides[dep] = lambda service=service: service
    return TestClient(app)

def test_endpoint_cadastro_unico_retorna_201_com_programas() -> None:
    service = CadastroUnicoService(cadastro_repo=InMemoryCadastroUnicoRepo(), citizen_service=FakeCitizenService(active=True), educacao_service=FakeEducacaoService(set()), juventude_service=FakeJuventudeService(set()), request_service=None)
    client = _build_client({get_cadastro_unico_service: service})
    response = client.post('/assistencia-social/cadastros-unicos/', json={'citizen_id_responsavel': str(uuid4()), 'renda_per_capita': '80.00', 'composicao_familiar': [{'idade': 4}, {'idade': 66}], 'condicoes_moradia': 'ALUGADA', 'acesso_agua': True, 'acesso_energia': True})
    assert response.status_code == 201
    payload = response.json()
    assert payload['cadastro']['codigo'].startswith('CAD/')
    assert 'BOLSA_FAMILIA' in payload['programas_elegiveis']
    assert 'BPC_IDOSO' in payload['programas_elegiveis']

def test_endpoint_obter_beneficiario_retorna_404_quando_nao_encontrado() -> None:
    service = SimpleNamespace(buscar_beneficiario=AsyncMock(side_effect=ValueError('Beneficiario nao encontrado')))
    client = _build_client({get_beneficiario_service: service})
    response = client.get(f'/assistencia-social/beneficiarios/{uuid4()}')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Beneficiario nao encontrado'

def test_endpoint_conceder_bpc_pcd_retorna_400_para_laudo_invalido() -> None:
    service = SimpleNamespace(conceder_bpc_pcd=AsyncMock(side_effect=ValueError('Laudo medico invalido para concessao de BPC')))
    client = _build_client({get_beneficio_service: service})
    response = client.post('/assistencia-social/beneficios/bpc-pcd', json={'beneficiario_id': str(uuid4()), 'pcd_id': str(uuid4()), 'valor': '706.00'})
    assert response.status_code == 400
    assert 'laudo' in response.json()['detail'].lower()

def test_endpoint_listar_beneficios_retorna_lista() -> None:
    beneficiario_id = uuid4()
    beneficio = Beneficio.solicitar(codigo='BNF/2026/000001', beneficiario_id=beneficiario_id, tipo=TipoBeneficio.AUXILIO_NUTRICIONAL, valor=Decimal('80.00'))
    service = SimpleNamespace(listar_beneficios=AsyncMock(return_value=[beneficio]))
    client = _build_client({get_beneficio_service: service})
    response = client.get(f'/assistencia-social/beneficios/?beneficiario_id={beneficiario_id}')
    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 1
    assert payload[0]['codigo'] == 'BNF/2026/000001'