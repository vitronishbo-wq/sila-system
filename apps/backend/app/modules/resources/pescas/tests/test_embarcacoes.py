from __future__ import annotations
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from apps.backend.app.modules.resources.pescas.api.deps import get_embarcacao_service
from apps.backend.app.modules.resources.pescas.api.endpoints.embarcacoes import router as embarcacoes_router
from apps.backend.app.modules.resources.pescas.application.services.embarcacao_service import EmbarcacaoService
from apps.backend.app.modules.resources.pescas.domain.enums import TipoEmbarcacao

@pytest.mark.asyncio
async def test_cadastrar_embarcacao_sucesso():
    repo = SimpleNamespace(next_inscricao=AsyncMock(return_value='LUANDA/2026/0001'), save=AsyncMock(side_effect=lambda item: item))
    citizen = SimpleNamespace(is_citizen_active=AsyncMock(return_value=True))
    request = SimpleNamespace(create_request=AsyncMock(return_value=uuid4()))
    service = EmbarcacaoService(repo, citizen, request)
    result = await service.cadastrar_embarcacao(nome='Mar Azul', tipo=TipoEmbarcacao.ARTESANAL, comprimento=Decimal('10.5'), arqueacao_bruta=Decimal('20.2'), porto_registro='LUANDA', proprietario_id=uuid4())
    assert result.numero_inscricao == 'LUANDA/2026/0001'

def test_endpoint_obter_embarcacao_404():
    service = SimpleNamespace(buscar_embarcacao=AsyncMock(side_effect=ValueError('Embarcacao nao encontrada')))
    app = FastAPI()
    app.include_router(embarcacoes_router, prefix='/pescas')
    app.dependency_overrides[get_embarcacao_service] = lambda: service
    client = TestClient(app)
    response = client.get(f'/pescas/embarcacoes/{uuid4()}')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Embarcacao nao encontrada'