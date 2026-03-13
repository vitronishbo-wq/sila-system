from __future__ import annotations
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.modules.society.seguranca_social.api.deps import get_pensao_service
from app.modules.society.seguranca_social.api.endpoints.pensoes import router as pensoes_router
from app.modules.society.seguranca_social.application.services.pensao_service import PensaoService
from app.modules.society.seguranca_social.domain.enums import RegimeSegurancaSocial, TipoBeneficiario, TipoPensao
from app.modules.society.seguranca_social.domain.models.beneficiario import Beneficiario
from app.modules.society.seguranca_social.domain.models.pensao import Pensao
from app.modules.society.seguranca_social.exceptions import BeneficiarioNotEligibleError, PensaoAlreadyExistsError, PensaoNotFoundError

def _build_service(pensao_repo, beneficiario_repo, request_service) -> PensaoService:
    return PensaoService(pensao_repo=pensao_repo, beneficiario_repo=beneficiario_repo, request_service=request_service)

@pytest.mark.asyncio
async def test_solicitar_pensao_sucesso():
    beneficiario = Beneficiario.criar(citizen_id=uuid4(), tipo=TipoBeneficiario.IDOSO, regime=RegimeSegurancaSocial.GERAL, numero_beneficiario='BEN/2026/0001')
    beneficiario.ativar()
    pensao_repo = SimpleNamespace(list_by_filtros=AsyncMock(return_value=[]), next_numero_processo=AsyncMock(return_value='PEN/2026/0001'), save=AsyncMock(side_effect=lambda pensao: pensao))
    beneficiario_repo = SimpleNamespace(get_by_id=AsyncMock(return_value=beneficiario))
    request_service = SimpleNamespace(create_request=AsyncMock(return_value=uuid4()), complete_request=AsyncMock(return_value=True))
    service = _build_service(pensao_repo, beneficiario_repo, request_service)
    result = await service.solicitar_pensao(beneficiario_id=beneficiario.id, tipo=TipoPensao.VELHICE, valor_mensal=Decimal('25000.00'))
    assert result.numero_processo == 'PEN/2026/0001'
    assert result.tipo == TipoPensao.VELHICE
    pensao_repo.save.assert_awaited_once()
    request_service.create_request.assert_awaited_once()

@pytest.mark.asyncio
async def test_solicitar_pensao_beneficiario_nao_ativo():
    beneficiario = Beneficiario.criar(citizen_id=uuid4(), tipo=TipoBeneficiario.IDOSO, regime=RegimeSegurancaSocial.GERAL, numero_beneficiario='BEN/2026/0005')
    pensao_repo = SimpleNamespace(list_by_filtros=AsyncMock(return_value=[]), next_numero_processo=AsyncMock(), save=AsyncMock())
    beneficiario_repo = SimpleNamespace(get_by_id=AsyncMock(return_value=beneficiario))
    request_service = SimpleNamespace(create_request=AsyncMock(), complete_request=AsyncMock())
    service = _build_service(pensao_repo, beneficiario_repo, request_service)
    with pytest.raises(BeneficiarioNotEligibleError):
        await service.solicitar_pensao(beneficiario_id=beneficiario.id, tipo=TipoPensao.VELHICE, valor_mensal=Decimal('15000.00'))

@pytest.mark.asyncio
async def test_aprovar_pensao_conclui_request():
    pensao = Pensao.solicitar(beneficiario_id=uuid4(), tipo=TipoPensao.INVALIDEZ, valor_mensal=Decimal('12000.00'), numero_processo='PEN/2026/0008')
    pensao_repo = SimpleNamespace(get_by_id=AsyncMock(return_value=pensao), save=AsyncMock(side_effect=lambda item: item))
    beneficiario_repo = SimpleNamespace(get_by_id=AsyncMock())
    request_service = SimpleNamespace(create_request=AsyncMock(return_value=uuid4()), complete_request=AsyncMock(return_value=True))
    service = _build_service(pensao_repo, beneficiario_repo, request_service)
    updated = await service.aprovar_pensao(pensao_id=pensao.id, actor_id=uuid4())
    assert updated.status.value == 'ativa'
    request_service.complete_request.assert_awaited_once()

@pytest.mark.asyncio
async def test_solicitar_pensao_bloqueia_duplicado_ativo():
    beneficiario = Beneficiario.criar(citizen_id=uuid4(), tipo=TipoBeneficiario.IDOSO, regime=RegimeSegurancaSocial.GERAL, numero_beneficiario='BEN/2026/0012')
    beneficiario.ativar()
    existente = Pensao.solicitar(beneficiario_id=beneficiario.id, tipo=TipoPensao.VELHICE, valor_mensal=Decimal('11111.00'), numero_processo='PEN/2026/0014')
    pensao_repo = SimpleNamespace(list_by_filtros=AsyncMock(return_value=[existente]), next_numero_processo=AsyncMock(), save=AsyncMock())
    beneficiario_repo = SimpleNamespace(get_by_id=AsyncMock(return_value=beneficiario))
    request_service = SimpleNamespace(create_request=AsyncMock(), complete_request=AsyncMock())
    service = _build_service(pensao_repo, beneficiario_repo, request_service)
    with pytest.raises(PensaoAlreadyExistsError):
        await service.solicitar_pensao(beneficiario_id=beneficiario.id, tipo=TipoPensao.VELHICE, valor_mensal=Decimal('22222.00'))

def _build_client(service) -> TestClient:
    app = FastAPI()
    app.include_router(pensoes_router, prefix='/seguranca-social')
    app.dependency_overrides[get_pensao_service] = lambda: service
    return TestClient(app)

def test_endpoint_solicitar_pensao_retorna_201():
    pensao = Pensao.solicitar(beneficiario_id=uuid4(), tipo=TipoPensao.VELHICE, valor_mensal=Decimal('30000.00'), numero_processo='PEN/2026/0002')
    service = SimpleNamespace(solicitar_pensao=AsyncMock(return_value=pensao))
    client = _build_client(service)
    response = client.post('/seguranca-social/pensoes/', json={'beneficiario_id': str(pensao.beneficiario_id), 'tipo': 'velhice', 'valor_mensal': '30000.00'})
    assert response.status_code == 201
    payload = response.json()
    assert payload['numero_processo'] == 'PEN/2026/0002'

def test_endpoint_aprovar_pensao_retorna_404_quando_inexistente():
    service = SimpleNamespace(aprovar_pensao=AsyncMock(side_effect=PensaoNotFoundError('nao encontrada')))
    client = _build_client(service)
    response = client.post(f'/seguranca-social/pensoes/{uuid4()}/aprovar', json={'actor_id': str(uuid4())})
    assert response.status_code == 404

def test_endpoint_solicitar_pensao_retorna_409_para_duplicado():
    service = SimpleNamespace(solicitar_pensao=AsyncMock(side_effect=PensaoAlreadyExistsError('duplicada')))
    client = _build_client(service)
    response = client.post('/seguranca-social/pensoes/', json={'beneficiario_id': str(uuid4()), 'tipo': 'velhice', 'valor_mensal': '30000.00'})
    assert response.status_code == 409