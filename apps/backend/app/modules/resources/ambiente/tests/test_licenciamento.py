from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from apps.backend.app.modules.resources.ambiente.api.deps import get_licenciamento_service
from apps.backend.app.modules.resources.ambiente.api.endpoints.licencas import (
    router as licencas_router,
)
from apps.backend.app.modules.resources.ambiente.application.services.cadastro_service import (
    CadastroService,
)
from apps.backend.app.modules.resources.ambiente.application.services.licenciamento_service import (
    LicenciamentoService,
)
from apps.backend.app.modules.resources.ambiente.domain.enums import (
    Bioma,
    StatusLicenca,
    TipoImovel,
    TipoLicenca,
)
from apps.backend.app.modules.resources.ambiente.exceptions import LicencaNotFoundError
from apps.backend.app.modules.resources.ambiente.infrastructure.repositories import (
    SQLAlchemyCARRepository,
    SQLAlchemyImovelRepository,
    SQLAlchemyLicencaRepository,
    SQLAlchemyProprietarioRepository,
)


@pytest.mark.asyncio
async def test_licenciamento_service_fluxo_requerer_deferir():
    proprietario_repo = SQLAlchemyProprietarioRepository()
    imovel_repo = SQLAlchemyImovelRepository()
    car_repo = SQLAlchemyCARRepository()
    licenca_repo = SQLAlchemyLicencaRepository()
    cadastro_service = CadastroService(
        proprietario_repo=proprietario_repo, imovel_repo=imovel_repo, car_repo=car_repo
    )
    licenciamento_service = LicenciamentoService(car_repo=car_repo, licenca_repo=licenca_repo)
    proprietario = await cadastro_service.cadastrar_proprietario(
        nome="Joao Kiala", documento="BI998877"
    )
    imovel = await cadastro_service.cadastrar_imovel(
        proprietario_id=proprietario.id,
        nome="Sitio Aurora",
        provincia="Bie",
        municipio="Kuito",
        area_total=Decimal("90"),
        bioma=Bioma.SAVANA,
        tipo_imovel=TipoImovel.PEQUENA_PROPRIEDADE,
    )
    car = await cadastro_service.criar_car(
        imovel_id=imovel.id,
        proprietario_id=proprietario.id,
        area_total=Decimal("90"),
        bioma=Bioma.SAVANA,
        tipo_imovel=TipoImovel.PEQUENA_PROPRIEDADE,
    )
    car = await cadastro_service.submeter_para_analise(car.numero_car)
    car = await cadastro_service.aprovar(car.numero_car, uuid4())
    licenca = await licenciamento_service.requerer_licenca(
        numero_car=car.numero_car,
        tipo=TipoLicenca.PREVIA,
        atividade="Implantacao de sistema de irrigacao",
    )
    assert licenca.status == StatusLicenca.REQUERIDA
    licenca = await licenciamento_service.iniciar_analise(licenca.numero_licenca)
    assert licenca.status == StatusLicenca.EM_ANALISE
    licenca = await licenciamento_service.deferir(
        licenca.numero_licenca,
        analista_id=uuid4(),
        data_validade=date.today() + timedelta(days=365),
        condicionantes=["Manter faixa de protecao"],
    )
    assert licenca.status == StatusLicenca.DEFERIDA


def test_endpoint_requerer_licenca_retorna_201():
    mock_item = SimpleNamespace(
        id=uuid4(),
        numero_licenca="LIC/2026/000001",
        numero_car="CAR/2026/000001",
        tipo=TipoLicenca.PREVIA,
        atividade="Irrigacao",
        status=StatusLicenca.REQUERIDA,
        data_requerimento=date(2026, 2, 28),
        data_analise=None,
        data_emissao=None,
        data_validade=None,
        analista_id=None,
        condicionantes=[],
        observacoes=None,
    )
    service = SimpleNamespace(requerer_licenca=AsyncMock(return_value=mock_item))
    app = FastAPI()
    app.include_router(licencas_router, prefix="/ambiente")
    app.dependency_overrides[get_licenciamento_service] = lambda: service
    client = TestClient(app)
    response = client.post(
        "/ambiente/licencas/",
        json={"numero_car": "CAR/2026/000001", "tipo": "previa", "atividade": "Irrigacao"},
    )
    assert response.status_code == 201
    assert response.json()["numero_licenca"] == "LIC/2026/000001"


def test_endpoint_obter_licenca_retorna_404():
    service = SimpleNamespace(
        obter_por_numero=AsyncMock(
            side_effect=LicencaNotFoundError("Licenca ambiental nao encontrada")
        )
    )
    app = FastAPI()
    app.include_router(licencas_router, prefix="/ambiente")
    app.dependency_overrides[get_licenciamento_service] = lambda: service
    client = TestClient(app)
    response = client.get("/ambiente/licencas/LIC/2026/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Licenca ambiental nao encontrada"
