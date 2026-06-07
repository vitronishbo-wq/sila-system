from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from apps.backend.app.modules.resources.ambiente.api.deps import get_penalidade_service
from apps.backend.app.modules.resources.ambiente.api.endpoints.autos_infracao import (
    router as autos_infracao_router,
)
from apps.backend.app.modules.resources.ambiente.api.endpoints.multas import router as multas_router
from apps.backend.app.modules.resources.ambiente.application.services.cadastro_service import (
    CadastroService,
)
from apps.backend.app.modules.resources.ambiente.application.services.fiscalizacao_service import (
    FiscalizacaoService,
)
from apps.backend.app.modules.resources.ambiente.application.services.licenciamento_service import (
    LicenciamentoService,
)
from apps.backend.app.modules.resources.ambiente.application.services.penalidade_service import (
    PenalidadeService,
)
from apps.backend.app.modules.resources.ambiente.domain.enums import (
    Bioma,
    StatusAutoInfracao,
    StatusEmbargo,
    StatusMulta,
    TipoAutoInfracao,
    TipoImovel,
    TipoLicenca,
)
from apps.backend.app.modules.resources.ambiente.exceptions import (
    AutoInfracaoNotFoundError,
    MultaNotFoundError,
)
from apps.backend.app.modules.resources.ambiente.infrastructure.repositories import (
    SQLAlchemyAutoInfracaoRepository,
    SQLAlchemyCARRepository,
    SQLAlchemyEmbargoRepository,
    SQLAlchemyFiscalizacaoRepository,
    SQLAlchemyImovelRepository,
    SQLAlchemyLicencaRepository,
    SQLAlchemyMultaRepository,
    SQLAlchemyProprietarioRepository,
)


@pytest.mark.asyncio
async def test_penalidade_service_fluxo_sucesso():
    proprietario_repo = SQLAlchemyProprietarioRepository()
    imovel_repo = SQLAlchemyImovelRepository()
    car_repo = SQLAlchemyCARRepository()
    licenca_repo = SQLAlchemyLicencaRepository()
    fiscalizacao_repo = SQLAlchemyFiscalizacaoRepository()
    auto_infracao_repo = SQLAlchemyAutoInfracaoRepository()
    embargo_repo = SQLAlchemyEmbargoRepository()
    multa_repo = SQLAlchemyMultaRepository()
    cadastro_service = CadastroService(
        proprietario_repo=proprietario_repo, imovel_repo=imovel_repo, car_repo=car_repo
    )
    licenciamento_service = LicenciamentoService(car_repo=car_repo, licenca_repo=licenca_repo)
    fiscalizacao_service = FiscalizacaoService(
        licenca_repo=licenca_repo, fiscalizacao_repo=fiscalizacao_repo
    )
    penalidade_service = PenalidadeService(
        fiscalizacao_repo=fiscalizacao_repo,
        auto_infracao_repo=auto_infracao_repo,
        embargo_repo=embargo_repo,
        multa_repo=multa_repo,
    )
    proprietario = await cadastro_service.cadastrar_proprietario(
        nome="Antonio Bungo", documento="BI55667788"
    )
    imovel = await cadastro_service.cadastrar_imovel(
        proprietario_id=proprietario.id,
        nome="Sitio Esperanca",
        provincia="Cuanza Sul",
        municipio="Sumbe",
        area_total=Decimal("60"),
        bioma=Bioma.SAVANA,
        tipo_imovel=TipoImovel.PEQUENA_PROPRIEDADE,
    )
    car = await cadastro_service.criar_car(
        imovel_id=imovel.id,
        proprietario_id=proprietario.id,
        area_total=Decimal("60"),
        bioma=Bioma.SAVANA,
        tipo_imovel=TipoImovel.PEQUENA_PROPRIEDADE,
    )
    car = await cadastro_service.submeter_para_analise(car.numero_car)
    car = await cadastro_service.aprovar(car.numero_car, uuid4())
    licenca = await licenciamento_service.requerer_licenca(
        numero_car=car.numero_car, tipo=TipoLicenca.PREVIA, atividade="Uso alternativo do solo"
    )
    licenca = await licenciamento_service.iniciar_analise(licenca.numero_licenca)
    licenca = await licenciamento_service.deferir(
        licenca.numero_licenca,
        analista_id=uuid4(),
        data_validade=date.today() + timedelta(days=365),
    )
    fiscalizacao = await fiscalizacao_service.agendar(
        numero_licenca=licenca.numero_licenca,
        localidade="Zona Leste",
        objetivo="Verificar supressao irregular",
        fiscal_responsavel="Fiscal B",
        data_agendada=date.today(),
    )
    fiscalizacao = await fiscalizacao_service.iniciar(fiscalizacao.numero_fiscalizacao)
    auto = await penalidade_service.lavrar_auto(
        numero_fiscalizacao=fiscalizacao.numero_fiscalizacao,
        tipo=TipoAutoInfracao.MULTA,
        descricao="Supressao de vegetacao sem autorizacao",
        fiscal_id=uuid4(),
        valor_multa=Decimal("15000.00"),
    )
    assert auto.status == StatusAutoInfracao.LAVRADO
    auto = await penalidade_service.notificar_auto(auto.numero_auto)
    auto = await penalidade_service.registrar_recurso_auto(auto.numero_auto)
    auto = await penalidade_service.julgar_auto(
        auto.numero_auto, mantido=True, observacoes="Penalidade mantida"
    )
    assert auto.status == StatusAutoInfracao.JULGADO
    embargo = await penalidade_service.aplicar_embargo(
        numero_auto_infracao=auto.numero_auto, motivo="Interromper atividade poluidora"
    )
    assert embargo.status == StatusEmbargo.ATIVO
    embargo = await penalidade_service.suspender_embargo(
        embargo.numero_embargo, motivo="Aguardando adequacao imediata"
    )
    assert embargo.status == StatusEmbargo.SUSPENSO
    embargo = await penalidade_service.levantar_embargo(
        embargo.numero_embargo, observacoes="Regularizacao comprovada"
    )
    assert embargo.status == StatusEmbargo.LEVANTADO
    multa = await penalidade_service.aplicar_multa(
        numero_auto_infracao=auto.numero_auto, valor=Decimal("15000.00"), dias_vencimento=45
    )
    assert multa.status == StatusMulta.APLICADA
    multa = await penalidade_service.parcelar_multa(multa.numero_multa, quantidade_parcelas=3)
    assert multa.status == StatusMulta.PARCELADA
    multa = await penalidade_service.registrar_pagamento_multa(multa.numero_multa)
    assert multa.status == StatusMulta.PAGA


def test_endpoint_lavrar_auto_retorna_201():
    mock_item = SimpleNamespace(
        id=uuid4(),
        numero_auto="AINF/2026/000001",
        numero_fiscalizacao="FIS/2026/000001",
        tipo=TipoAutoInfracao.MULTA,
        descricao="Auto lavrado",
        fiscal_id=uuid4(),
        status=StatusAutoInfracao.LAVRADO,
        data_lavratura=date(2026, 2, 28),
        valor_multa=Decimal("5000.00"),
        observacoes=None,
    )
    service = SimpleNamespace(lavrar_auto=AsyncMock(return_value=mock_item))
    app = FastAPI()
    app.include_router(autos_infracao_router, prefix="/ambiente")
    app.dependency_overrides[get_penalidade_service] = lambda: service
    client = TestClient(app)
    response = client.post(
        "/ambiente/autos-infracao/",
        json={
            "numero_fiscalizacao": "FIS/2026/000001",
            "tipo": "multa",
            "descricao": "Auto lavrado",
            "fiscal_id": str(uuid4()),
            "valor_multa": "5000.00",
        },
    )
    assert response.status_code == 201
    assert response.json()["numero_auto"] == "AINF/2026/000001"


def test_endpoint_obter_auto_retorna_404():
    service = SimpleNamespace(
        obter_auto_por_numero=AsyncMock(
            side_effect=AutoInfracaoNotFoundError("Auto de infracao nao encontrado")
        )
    )
    app = FastAPI()
    app.include_router(autos_infracao_router, prefix="/ambiente")
    app.dependency_overrides[get_penalidade_service] = lambda: service
    client = TestClient(app)
    response = client.get("/ambiente/autos-infracao/AINF/2026/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Auto de infracao nao encontrado"


def test_endpoint_obter_multa_retorna_404():
    service = SimpleNamespace(
        obter_multa_por_numero=AsyncMock(side_effect=MultaNotFoundError("Multa nao encontrada"))
    )
    app = FastAPI()
    app.include_router(multas_router, prefix="/ambiente")
    app.dependency_overrides[get_penalidade_service] = lambda: service
    client = TestClient(app)
    response = client.get("/ambiente/multas/MULT/2026/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Multa nao encontrada"
