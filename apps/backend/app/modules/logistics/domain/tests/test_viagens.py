from __future__ import annotations
from datetime import datetime, timedelta
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.modules.logistics.api.deps import get_viagem_service
from app.modules.logistics.api.endpoints.viagens import router as viagens_router
from app.modules.logistics.application.services import ViagemService
from app.modules.logistics.domain.enums import StatusViagem
from app.modules.logistics.domain.models import Viagem
from app.modules.logistics.core.exceptions import ViagemConflictError, ViagemNotFoundError
from app.modules.logistics.infrastructure.repositories import SQLAlchemyViagemRepository

@pytest.mark.asyncio
async def test_viagem_service_fluxo_sucesso():
    service = ViagemService(viagem_repo=SQLAlchemyViagemRepository())
    saida = datetime.utcnow()
    chegada_prevista = saida + timedelta(hours=2)
    viagem = await service.programar_viagem(linha_id=uuid4(), veiculo_id=uuid4(), motorista_id=uuid4(), data_hora_saida=saida, data_hora_chegada_prevista=chegada_prevista, origem='Luanda', destino='Bengo', itinerario=[{'ordem': 1, 'ponto': 'Cacuaco'}])
    assert viagem.status == StatusViagem.PROGRAMADA
    viagem = await service.iniciar_viagem(viagem.id)
    assert viagem.status == StatusViagem.EM_ANDAMENTO
    viagem = await service.concluir_viagem(viagem.id, data_hora_chegada=chegada_prevista)
    assert viagem.status == StatusViagem.CONCLUIDA
    assert viagem.data_hora_chegada_real == chegada_prevista

@pytest.mark.asyncio
async def test_viagem_service_detecta_conflito_de_veiculo():
    service = ViagemService(viagem_repo=SQLAlchemyViagemRepository())
    veiculo_id = uuid4()
    base = datetime.utcnow()
    await service.programar_viagem(linha_id=uuid4(), veiculo_id=veiculo_id, motorista_id=uuid4(), data_hora_saida=base, data_hora_chegada_prevista=base + timedelta(hours=3), origem='Luanda', destino='Viana')
    with pytest.raises(ViagemConflictError):
        await service.programar_viagem(linha_id=uuid4(), veiculo_id=veiculo_id, motorista_id=uuid4(), data_hora_saida=base + timedelta(hours=1), data_hora_chegada_prevista=base + timedelta(hours=4), origem='Luanda', destino='Caxito')

def test_endpoint_programar_viagem_retorna_201():
    viagem = Viagem.programar(linha_id=uuid4(), veiculo_id=uuid4(), motorista_id=uuid4(), data_hora_saida=datetime(2026, 3, 1, 8, 0, 0), data_hora_chegada_prevista=datetime(2026, 3, 1, 10, 0, 0), origem='Luanda', destino='Bengo', itinerario=[{'ordem': 1, 'ponto': 'Cacuaco'}])
    service = SimpleNamespace(programar_viagem=AsyncMock(return_value=viagem))
    app = FastAPI()
    app.include_router(viagens_router, prefix='/transportes-logistica')
    app.dependency_overrides[get_viagem_service] = lambda: service
    client = TestClient(app)
    response = client.post('/transportes-logistica/viagens/', json={'linha_id': str(viagem.linha_id), 'veiculo_id': str(viagem.veiculo_id), 'motorista_id': str(viagem.motorista_id), 'data_hora_saida': '2026-03-01T08:00:00', 'data_hora_chegada_prevista': '2026-03-01T10:00:00', 'origem': 'Luanda', 'destino': 'Bengo', 'itinerario': [{'ordem': 1, 'ponto': 'Cacuaco'}]})
    assert response.status_code == 201
    assert response.json()['status'] == 'programada'

def test_endpoint_obter_viagem_retorna_404():
    service = SimpleNamespace(obter_por_id=AsyncMock(side_effect=ViagemNotFoundError('Viagem nao encontrada')))
    app = FastAPI()
    app.include_router(viagens_router, prefix='/transportes-logistica')
    app.dependency_overrides[get_viagem_service] = lambda: service
    client = TestClient(app)
    response = client.get(f'/transportes-logistica/viagens/{uuid4()}')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Viagem nao encontrada'
