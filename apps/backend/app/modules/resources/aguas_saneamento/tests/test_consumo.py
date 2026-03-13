from __future__ import annotations
from datetime import date
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from apps.backend.app.modules.resources.aguas_saneamento.api.deps import get_consumo_service
from apps.backend.app.modules.resources.aguas_saneamento.api.endpoints.consumo import router as consumo_router
from apps.backend.app.modules.resources.aguas_saneamento.application.services.consumo_service import ConsumoService
from apps.backend.app.modules.resources.aguas_saneamento.domain.enums import CategoriaConsumo, StatusConsumo
from apps.backend.app.modules.resources.aguas_saneamento.exceptions import ConsumoNotFoundError
from apps.backend.app.modules.resources.aguas_saneamento.infrastructure.repositories import SQLAlchemyConsumoRepository

@pytest.mark.asyncio
async def test_consumo_service_fluxo_sucesso():
    service = ConsumoService(consumo_repo=SQLAlchemyConsumoRepository())
    item = await service.registrar(abastecimento_id=uuid4(), titular_id=uuid4(), referencia='2026-03', categoria=CategoriaConsumo.RESIDENCIAL, volume_m3=Decimal('18.75'), unidade_volume='m3', leitura_anterior=Decimal('100.00'), leitura_atual=Decimal('118.75'))
    assert item.status == StatusConsumo.REGISTRADO
    item = await service.validar(item.codigo_consumo)
    assert item.status == StatusConsumo.VALIDADO
    item = await service.faturar(item.codigo_consumo)
    assert item.status == StatusConsumo.FATURADO

def test_endpoint_registrar_consumo_retorna_201():
    mock_item = SimpleNamespace(id=uuid4(), codigo_consumo='CON/2026/000001', abastecimento_id=uuid4(), titular_id=uuid4(), referencia='2026-03', categoria=CategoriaConsumo.RESIDENCIAL, volume_m3=Decimal('18.75'), unidade_volume='m3', data_leitura=date(2026, 3, 1), status=StatusConsumo.REGISTRADO, data_registro=date(2026, 3, 1), hidrometro_id=None, leitura_anterior=Decimal('100.00'), leitura_atual=Decimal('118.75'), observacoes=None)
    service = SimpleNamespace(registrar=AsyncMock(return_value=mock_item))
    app = FastAPI()
    app.include_router(consumo_router, prefix='/aguas-saneamento')
    app.dependency_overrides[get_consumo_service] = lambda: service
    client = TestClient(app)
    response = client.post('/aguas-saneamento/consumo/', json={'abastecimento_id': str(uuid4()), 'titular_id': str(uuid4()), 'referencia': '2026-03', 'categoria': 'residencial', 'volume_m3': '18.75', 'unidade_volume': 'm3', 'leitura_anterior': '100.00', 'leitura_atual': '118.75'})
    assert response.status_code == 201
    assert response.json()['codigo_consumo'] == 'CON/2026/000001'

def test_endpoint_obter_consumo_retorna_404():
    service = SimpleNamespace(obter_por_codigo=AsyncMock(side_effect=ConsumoNotFoundError('Consumo nao encontrado')))
    app = FastAPI()
    app.include_router(consumo_router, prefix='/aguas-saneamento')
    app.dependency_overrides[get_consumo_service] = lambda: service
    client = TestClient(app)
    response = client.get('/aguas-saneamento/consumo/CON/2026/999999')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Consumo nao encontrado'