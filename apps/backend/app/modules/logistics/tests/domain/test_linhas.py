from __future__ import annotations

from datetime import date
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from apps.backend.app.modules.logistics.api.deps import get_linha_service
from apps.backend.app.modules.logistics.api.endpoints.linhas import router as linhas_router
from apps.backend.app.modules.logistics.application.services import LinhaService
from apps.backend.app.modules.logistics.domain.enums import (
    ModalTransporte,
    StatusLinha,
    TipoVeiculo,
    TipoViagem,
)
from apps.backend.app.modules.logistics.domain.models import Linha
from apps.backend.app.modules.logistics.infrastructure.repositories import (
    SQLAlchemyLinhaRepository,
    SQLAlchemyVeiculoRepository,
)


@pytest.mark.asyncio
async def test_linha_service_fluxo_completo():
    geosampa_adapter = SimpleNamespace(rota_valida=AsyncMock(return_value=True))
    urbanismo_adapter = SimpleNamespace(validar_zoneamento_rota=AsyncMock(return_value=True))
    obras_adapter = SimpleNamespace(validar_corredor=AsyncMock(return_value=True))
    workflow_adapter = SimpleNamespace(
        iniciar_fluxo=AsyncMock(return_value="WF-TRN-LIN-001"),
        registrar_evento=AsyncMock(return_value=None),
    )
    service = LinhaService(
        linha_repo=SQLAlchemyLinhaRepository(),
        veiculo_repo=SQLAlchemyVeiculoRepository(),
        geosampa_adapter=geosampa_adapter,
        urbanismo_adapter=urbanismo_adapter,
        obras_publicas_adapter=obras_adapter,
        workflow_adapter=workflow_adapter,
    )
    veiculo = await service.cadastrar_veiculo(
        placa="LD-10-20-AA",
        tipo=TipoVeiculo.ONIBUS,
        marca="Volvo",
        modelo="B340",
        ano_fabricacao=2022,
        ano_modelo=2023,
        proprietario_id=uuid4(),
        proprietario_tipo="cnpj",
        data_aquisicao=date(2025, 1, 15),
        capacidade_passageiros=70,
        operadora_id=uuid4(),
    )
    linha = await service.criar_linha(
        nome="Linha Centro",
        modal=ModalTransporte.RODOVIARIO,
        tipo_viagem=TipoViagem.URBANA,
        origem="Centro",
        destino="Viana",
        itinerario=[{"ponto": "Mutamba"}, {"ponto": "Cazenga"}],
        extensao_km=Decimal("18.50"),
        tempo_estimado_minutos=60,
        dias_operacao=["seg", "ter", "qua", "qui", "sex"],
        horario_inicio="05:30",
        horario_fim="22:00",
        tarifa_base=Decimal("250.00"),
        operadora_id=uuid4(),
        codigo_corredor="CRD-NORTE-01",
    )
    assert linha.status == StatusLinha.EM_IMPLANTACAO
    linha = await service.vincular_veiculo(linha.codigo, placa=veiculo.placa)
    assert linha.status == StatusLinha.ATIVA
    assert len(linha.veiculos_ativos) == 1
    linha = await service.atualizar_tarifa(linha.codigo, valor=Decimal("280.00"))
    assert linha.tarifa_base == Decimal("280.00")
    linha = await service.registrar_indicadores(
        linha.codigo,
        demanda_media_diaria=1200,
        ocupacao_media=Decimal("73.25"),
        regularidade=Decimal("96.00"),
        pontualidade=Decimal("93.40"),
    )
    assert linha.demanda_media_diaria == 1200
    assert linha.pontualidade == Decimal("93.40")
    geosampa_adapter.rota_valida.assert_awaited_once()
    urbanismo_adapter.validar_zoneamento_rota.assert_awaited_once()
    obras_adapter.validar_corredor.assert_awaited_once()
    workflow_adapter.iniciar_fluxo.assert_awaited_once()
    workflow_adapter.registrar_evento.assert_awaited()


def test_endpoint_criar_linha_retorna_201():
    linha = Linha.criar(
        codigo="LIN/2026/000001",
        nome="Linha Centro",
        modal=ModalTransporte.RODOVIARIO,
        tipo_viagem=TipoViagem.URBANA,
        origem="Centro",
        destino="Viana",
        itinerario=[{"ponto": "Mutamba"}],
        extensao_km=Decimal("12.00"),
        tempo_estimado_minutos=45,
        dias_operacao=["seg", "ter"],
        horario_inicio="05:30",
        horario_fim="22:00",
        tarifa_base=Decimal("250.00"),
        operadora_id=uuid4(),
    )
    service = SimpleNamespace(criar_linha=AsyncMock(return_value=linha))
    service.has_geosampa_adapter = lambda: True
    service.has_urbanismo_adapter = lambda: True
    service.has_workflow_adapter = lambda: True
    app = FastAPI()
    app.include_router(linhas_router, prefix="/transportes-logistica")
    app.dependency_overrides[get_linha_service] = lambda: service
    client = TestClient(app)
    response = client.post(
        "/transportes-logistica/linhas/",
        json={
            "nome": "Linha Centro",
            "modal": "rodoviario",
            "tipo_viagem": "urbana",
            "origem": "Centro",
            "destino": "Viana",
            "itinerario": [{"ponto": "Mutamba"}],
            "extensao_km": "12.00",
            "tempo_estimado_minutos": 45,
            "dias_operacao": ["seg", "ter"],
            "horario_inicio": "05:30",
            "horario_fim": "22:00",
            "tarifa_base": "250.00",
            "operadora_id": str(uuid4()),
        },
    )
    assert response.status_code == 201
    assert response.json()["codigo"] == "LIN/2026/000001"


def test_endpoint_criar_linha_sem_geosampa_retorna_503():
    service = SimpleNamespace(criar_linha=AsyncMock())
    service.has_geosampa_adapter = lambda: False
    service.has_urbanismo_adapter = lambda: True
    service.has_workflow_adapter = lambda: True
    app = FastAPI()
    app.include_router(linhas_router, prefix="/transportes-logistica")
    app.dependency_overrides[get_linha_service] = lambda: service
    client = TestClient(app)
    response = client.post(
        "/transportes-logistica/linhas/",
        json={
            "nome": "Linha Centro",
            "modal": "rodoviario",
            "tipo_viagem": "urbana",
            "origem": "Centro",
            "destino": "Viana",
            "itinerario": [{"ponto": "Mutamba"}],
            "extensao_km": "12.00",
            "tempo_estimado_minutos": 45,
            "dias_operacao": ["seg", "ter"],
            "horario_inicio": "05:30",
            "horario_fim": "22:00",
            "tarifa_base": "250.00",
            "operadora_id": str(uuid4()),
        },
    )
    assert response.status_code == 503
    assert "Geosampa indisponivel" in response.json()["detail"]
    service.criar_linha.assert_not_awaited()
