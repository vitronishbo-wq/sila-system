from __future__ import annotations

from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from apps.backend.app.modules.logistics.api.deps import get_bilhetagem_service
from apps.backend.app.modules.logistics.api.endpoints.bilhetagem import router as bilhetagem_router
from apps.backend.app.modules.logistics.application.services import BilhetagemService
from apps.backend.app.modules.logistics.domain.enums import (
    StatusReconciliacaoFinanceira,
    TipoTarifa,
)
from apps.backend.app.modules.logistics.domain.models import BilhetagemEletronica
from apps.backend.app.modules.logistics.infrastructure.repositories import (
    SQLAlchemyBilhetagemRepository,
)


@pytest.mark.asyncio
async def test_bilhetagem_service_registro_e_reconciliacao():
    financas_adapter = SimpleNamespace(
        registrar_receita_bilhetagem=AsyncMock(return_value="REC-TRN-0001"),
        reconciliar_lancamento=AsyncMock(return_value=True),
    )
    workflow_adapter = SimpleNamespace(registrar_evento=AsyncMock(return_value=None))
    service = BilhetagemService(
        bilhetagem_repo=SQLAlchemyBilhetagemRepository(),
        financas_adapter=financas_adapter,
        workflow_adapter=workflow_adapter,
    )
    evento = await service.registrar_evento(
        codigo_bilhete="BILH-0001",
        viagem_id=uuid4(),
        tipo_tarifa=TipoTarifa.PUBLICA,
        valor_pago=Decimal("250.00"),
        forma_pagamento="cartao",
    )
    assert evento.lancamento_financeiro_id == "REC-TRN-0001"
    assert evento.status_reconciliacao == StatusReconciliacaoFinanceira.PENDENTE
    reconciliado = await service.reconciliar_evento(
        evento.id, confirmado=True, referencia_externa="BANK-REF-001"
    )
    assert reconciliado.status_reconciliacao == StatusReconciliacaoFinanceira.CONFIRMADO
    assert reconciliado.referencia_externa == "BANK-REF-001"
    financas_adapter.registrar_receita_bilhetagem.assert_awaited_once()
    financas_adapter.reconciliar_lancamento.assert_awaited_once()
    workflow_adapter.registrar_evento.assert_awaited()


def test_endpoint_registrar_evento_bilhetagem_retorna_201():
    evento = BilhetagemEletronica.registrar_evento(
        codigo_bilhete="BILH-0001",
        viagem_id=uuid4(),
        tipo_tarifa=TipoTarifa.PUBLICA,
        valor_pago=Decimal("250.00"),
        forma_pagamento="cartao",
    )
    evento.vincular_lancamento("REC-TRN-0001")
    service = SimpleNamespace(registrar_evento=AsyncMock(return_value=evento))
    service.has_financas_adapter = lambda: True
    app = FastAPI()
    app.include_router(bilhetagem_router, prefix="/transportes-logistica")
    app.dependency_overrides[get_bilhetagem_service] = lambda: service
    client = TestClient(app)
    response = client.post(
        "/transportes-logistica/bilhetagem/eventos",
        json={
            "codigo_bilhete": "BILH-0001",
            "viagem_id": str(uuid4()),
            "tipo_tarifa": "publica",
            "valor_pago": "250.00",
            "forma_pagamento": "cartao",
            "metadata": {"catraca": "A1"},
        },
    )
    assert response.status_code == 201
    assert response.json()["codigo_bilhete"] == "BILH-0001"


def test_endpoint_registrar_evento_sem_financas_retorna_503():
    service = SimpleNamespace(registrar_evento=AsyncMock())
    service.has_financas_adapter = lambda: False
    app = FastAPI()
    app.include_router(bilhetagem_router, prefix="/transportes-logistica")
    app.dependency_overrides[get_bilhetagem_service] = lambda: service
    client = TestClient(app)
    response = client.post(
        "/transportes-logistica/bilhetagem/eventos",
        json={
            "codigo_bilhete": "BILH-0001",
            "viagem_id": str(uuid4()),
            "tipo_tarifa": "publica",
            "valor_pago": "250.00",
            "forma_pagamento": "cartao",
            "metadata": {"catraca": "A1"},
        },
    )
    assert response.status_code == 503
    assert "Financas indisponivel" in response.json()["detail"]
    service.registrar_evento.assert_not_awaited()
