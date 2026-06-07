from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from apps.backend.app.modules.resources.agricultura.api.deps import get_plantio_service
from apps.backend.app.modules.resources.agricultura.api.endpoints.plantios import (
    router as plantios_router,
)
from apps.backend.app.modules.resources.agricultura.application.services.plantio_service import (
    PlantioService,
)
from apps.backend.app.modules.resources.agricultura.application.services.producao_service import (
    ProducaoService,
)
from apps.backend.app.modules.resources.agricultura.application.services.propriedade_service import (
    PropriedadeService,
)
from apps.backend.app.modules.resources.agricultura.application.services.safra_service import (
    SafraService,
)
from apps.backend.app.modules.resources.agricultura.application.services.talhao_service import (
    TalhaoService,
)
from apps.backend.app.modules.resources.agricultura.domain.enums import (
    StatusPlantio,
    TipoCultura,
    TipoPropriedade,
)
from apps.backend.app.modules.resources.agricultura.exceptions import PlantioNotFoundError


@pytest.mark.asyncio
async def test_plantio_service_planejar_e_executar():
    propriedade_service = PropriedadeService()
    producao_service = ProducaoService()
    safra_service = SafraService(
        propriedade_service=propriedade_service, producao_service=producao_service
    )
    talhao_service = TalhaoService(propriedade_service=propriedade_service)
    prop = await propriedade_service.cadastrar(
        produtor_id=uuid4(),
        nome="Fazenda Plantio",
        tipo=TipoPropriedade.PROPRIO,
        area_total_ha=80,
        area_cultivavel_ha=60,
    )
    talhao = await talhao_service.cadastrar(
        codigo_propriedade=prop.codigo_propriedade, nome="Talhao A", area_ha=15
    )
    cultura = await producao_service.cadastrar_cultura(
        nome="Soja", tipo=TipoCultura.GRAOS, ciclo_dias=100, produtividade_estimada_ton_ha=2.4
    )
    safra = await safra_service.criar_safra(
        codigo_propriedade=prop.codigo_propriedade,
        codigo_cultura=cultura.codigo_cultura,
        ano=2026,
        area_plantada_ha=15,
        producao_estimada_ton=35,
    )
    service = PlantioService(safra_service=safra_service, talhao_service=talhao_service)
    plantio = await service.planejar(
        codigo_safra=safra.codigo_safra,
        codigo_talhao=talhao.codigo_talhao,
        area_plantada_ha=10,
        quantidade_semente=280,
    )
    assert plantio.status == StatusPlantio.PLANEJADO
    plantio = await service.executar(plantio.codigo_plantio)
    assert plantio.status == StatusPlantio.EXECUTADO


def test_endpoint_planejar_plantio_retorna_201():
    mock_item = SimpleNamespace(
        id=uuid4(),
        codigo_plantio="PLA/2026/000001",
        codigo_safra="SAF/2026/000001",
        codigo_talhao="TAL/2026/000001",
        area_plantada_ha=10.0,
        quantidade_semente=280.0,
        data_planejamento="2026-02-28",
        status="planejado",
        data_execucao=None,
        motivo_cancelamento=None,
    )
    service = SimpleNamespace(planejar=AsyncMock(return_value=mock_item))
    app = FastAPI()
    app.include_router(plantios_router, prefix="/agricultura")
    app.dependency_overrides[get_plantio_service] = lambda: service
    client = TestClient(app)
    response = client.post(
        "/agricultura/plantios/",
        json={
            "codigo_safra": "SAF/2026/000001",
            "codigo_talhao": "TAL/2026/000001",
            "area_plantada_ha": 10,
            "quantidade_semente": 280,
        },
    )
    assert response.status_code == 201
    assert response.json()["codigo_plantio"] == "PLA/2026/000001"


def test_endpoint_obter_plantio_retorna_404():
    service = SimpleNamespace(
        obter=AsyncMock(side_effect=PlantioNotFoundError("Plantio nao encontrado"))
    )
    app = FastAPI()
    app.include_router(plantios_router, prefix="/agricultura")
    app.dependency_overrides[get_plantio_service] = lambda: service
    client = TestClient(app)
    response = client.get("/agricultura/plantios/PLA/2026/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Plantio nao encontrado"
