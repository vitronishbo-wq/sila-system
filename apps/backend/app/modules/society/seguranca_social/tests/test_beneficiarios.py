from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from apps.backend.app.modules.society.seguranca_social.api.deps import get_beneficiario_service
from apps.backend.app.modules.society.seguranca_social.api.endpoints.beneficiarios import (
    router as beneficiarios_router,
)
from apps.backend.app.modules.society.seguranca_social.application.services.beneficiario_service import (
    BeneficiarioService,
)
from apps.backend.app.modules.society.seguranca_social.domain.enums import (
    EstadoBeneficiario,
    RegimeSegurancaSocial,
    TipoBeneficiario,
)
from apps.backend.app.modules.society.seguranca_social.domain.models.beneficiario import (
    Beneficiario,
)
from apps.backend.app.modules.society.seguranca_social.exceptions import (
    BeneficiarioAlreadyExistsError,
    CandidatoEmpregoRequiredError,
    CitizenNotFoundError,
)


def _build_service(
    beneficiario_repo, citizen_repo, emprego_service, request_service
) -> BeneficiarioService:
    return BeneficiarioService(
        beneficiario_repo=beneficiario_repo,
        citizen_repo=citizen_repo,
        emprego_service=emprego_service,
        request_service=request_service,
    )


@pytest.mark.asyncio
async def test_inscrever_beneficiario_sucesso():
    citizen_id = uuid4()
    beneficiario_repo = SimpleNamespace(
        get_by_citizen=AsyncMock(return_value=None),
        next_numero_beneficiario=AsyncMock(return_value="BEN/2026/0001"),
        save=AsyncMock(side_effect=lambda beneficiario: beneficiario),
    )
    citizen_repo = SimpleNamespace(get_citizen=AsyncMock(return_value={"id": citizen_id}))
    emprego_service = SimpleNamespace(is_candidato_registrado=AsyncMock(return_value=True))
    request_service = SimpleNamespace(
        create_request=AsyncMock(return_value=uuid4()),
        complete_request=AsyncMock(return_value=True),
    )
    service = _build_service(beneficiario_repo, citizen_repo, emprego_service, request_service)
    result = await service.inscrever_beneficiario(
        citizen_id=citizen_id, tipo=TipoBeneficiario.IDOSO, regime=RegimeSegurancaSocial.GERAL
    )
    assert result.numero_beneficiario == "BEN/2026/0001"
    assert result.estado == EstadoBeneficiario.PENDENTE
    beneficiario_repo.save.assert_awaited_once()
    request_service.create_request.assert_awaited_once()


@pytest.mark.asyncio
async def test_inscrever_beneficiario_cidadao_inexistente():
    beneficiario_repo = SimpleNamespace(
        get_by_citizen=AsyncMock(), next_numero_beneficiario=AsyncMock(), save=AsyncMock()
    )
    citizen_repo = SimpleNamespace(get_citizen=AsyncMock(return_value=None))
    emprego_service = SimpleNamespace(is_candidato_registrado=AsyncMock(return_value=False))
    request_service = SimpleNamespace(create_request=AsyncMock(), complete_request=AsyncMock())
    service = _build_service(beneficiario_repo, citizen_repo, emprego_service, request_service)
    with pytest.raises(CitizenNotFoundError):
        await service.inscrever_beneficiario(
            citizen_id=uuid4(), tipo=TipoBeneficiario.IDOSO, regime=RegimeSegurancaSocial.GERAL
        )


@pytest.mark.asyncio
async def test_inscrever_beneficiario_bloqueia_duplicado_ativo_ou_pendente():
    citizen_id = uuid4()
    existente = Beneficiario.criar(
        citizen_id=citizen_id,
        tipo=TipoBeneficiario.TRABALHADOR,
        regime=RegimeSegurancaSocial.GERAL,
        numero_beneficiario="BEN/2026/0004",
    )
    beneficiario_repo = SimpleNamespace(
        get_by_citizen=AsyncMock(return_value=existente),
        next_numero_beneficiario=AsyncMock(),
        save=AsyncMock(),
    )
    citizen_repo = SimpleNamespace(get_citizen=AsyncMock(return_value={"id": citizen_id}))
    emprego_service = SimpleNamespace(is_candidato_registrado=AsyncMock(return_value=True))
    request_service = SimpleNamespace(create_request=AsyncMock(), complete_request=AsyncMock())
    service = _build_service(beneficiario_repo, citizen_repo, emprego_service, request_service)
    with pytest.raises(BeneficiarioAlreadyExistsError):
        await service.inscrever_beneficiario(
            citizen_id=citizen_id,
            tipo=TipoBeneficiario.TRABALHADOR,
            regime=RegimeSegurancaSocial.GERAL,
        )


@pytest.mark.asyncio
async def test_inscrever_beneficiario_desempregado_exige_candidato_emprego():
    citizen_id = uuid4()
    beneficiario_repo = SimpleNamespace(
        get_by_citizen=AsyncMock(return_value=None),
        next_numero_beneficiario=AsyncMock(),
        save=AsyncMock(),
    )
    citizen_repo = SimpleNamespace(get_citizen=AsyncMock(return_value={"id": citizen_id}))
    emprego_service = SimpleNamespace(is_candidato_registrado=AsyncMock(return_value=False))
    request_service = SimpleNamespace(create_request=AsyncMock(), complete_request=AsyncMock())
    service = _build_service(beneficiario_repo, citizen_repo, emprego_service, request_service)
    with pytest.raises(CandidatoEmpregoRequiredError):
        await service.inscrever_beneficiario(
            citizen_id=citizen_id,
            tipo=TipoBeneficiario.DESEMPREGADO,
            regime=RegimeSegurancaSocial.GERAL,
        )


@pytest.mark.asyncio
async def test_ativar_beneficiario_conclui_request():
    citizen_id = uuid4()
    beneficiario = Beneficiario.criar(
        citizen_id=citizen_id,
        tipo=TipoBeneficiario.IDOSO,
        regime=RegimeSegurancaSocial.GERAL,
        numero_beneficiario="BEN/2026/0010",
    )
    beneficiario_repo = SimpleNamespace(
        get_by_id=AsyncMock(return_value=beneficiario),
        save=AsyncMock(side_effect=lambda item: item),
    )
    citizen_repo = SimpleNamespace(get_citizen=AsyncMock())
    emprego_service = SimpleNamespace(is_candidato_registrado=AsyncMock())
    request_service = SimpleNamespace(
        create_request=AsyncMock(return_value=uuid4()),
        complete_request=AsyncMock(return_value=True),
    )
    service = _build_service(beneficiario_repo, citizen_repo, emprego_service, request_service)
    updated = await service.ativar_beneficiario(beneficiario_id=beneficiario.id)
    assert updated.estado == EstadoBeneficiario.ATIVO
    request_service.complete_request.assert_awaited_once()


def _build_client(service) -> TestClient:
    app = FastAPI()
    app.include_router(beneficiarios_router, prefix="/seguranca-social")
    app.dependency_overrides[get_beneficiario_service] = lambda: service
    return TestClient(app)


def test_endpoint_inscrever_beneficiario_retorna_201():
    citizen_id = uuid4()
    beneficiario = Beneficiario.criar(
        citizen_id=citizen_id,
        tipo=TipoBeneficiario.IDOSO,
        regime=RegimeSegurancaSocial.GERAL,
        numero_beneficiario="BEN/2026/0002",
    )
    service = SimpleNamespace(inscrever_beneficiario=AsyncMock(return_value=beneficiario))
    client = _build_client(service)
    response = client.post(
        "/seguranca-social/beneficiarios/",
        json={"citizen_id": str(citizen_id), "tipo": "idoso", "regime": "geral"},
    )
    assert response.status_code == 201
    payload = response.json()
    assert payload["numero_beneficiario"] == "BEN/2026/0002"
    assert payload["estado"] == "pendente"


def test_endpoint_inscrever_beneficiario_retorna_409_para_duplicado():
    service = SimpleNamespace(
        inscrever_beneficiario=AsyncMock(side_effect=BeneficiarioAlreadyExistsError("ja existe"))
    )
    client = _build_client(service)
    response = client.post(
        "/seguranca-social/beneficiarios/",
        json={"citizen_id": str(uuid4()), "tipo": "idoso", "regime": "geral"},
    )
    assert response.status_code == 409
