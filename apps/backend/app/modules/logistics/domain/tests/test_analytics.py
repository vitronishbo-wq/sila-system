from __future__ import annotations
from datetime import datetime, timedelta
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from apps.backend.app.modules.logistics.api.deps import get_operacao_analytics_service
from apps.backend.app.modules.logistics.api.endpoints.analytics import router as analytics_router
from apps.backend.app.modules.logistics.application.services import OperacaoAnalyticsService
from apps.backend.app.modules.logistics.domain.enums import TipoTarifa
from apps.backend.app.modules.logistics.domain.models import BilhetagemEletronica, Viagem
from apps.backend.app.modules.logistics.infrastructure.repositories import SQLAlchemyBilhetagemRepository, SQLAlchemyViagemRepository

@pytest.mark.asyncio
async def test_operacao_analytics_calcula_demanda_e_qualidade():
    viagem_repo = SQLAlchemyViagemRepository()
    bilhetagem_repo = SQLAlchemyBilhetagemRepository()
    service = OperacaoAnalyticsService(viagem_repo=viagem_repo, bilhetagem_repo=bilhetagem_repo)
    base = datetime.utcnow()
    viagem_1 = Viagem.programar(linha_id=uuid4(), veiculo_id=uuid4(), motorista_id=uuid4(), data_hora_saida=base, data_hora_chegada_prevista=base + timedelta(minutes=40), origem='Centro', destino='Viana')
    viagem_1.passageiros_embarcados = 120
    viagem_1.iniciar()
    viagem_1.concluir(base + timedelta(minutes=38))
    await viagem_repo.save(viagem_1)
    viagem_2 = Viagem.programar(linha_id=viagem_1.linha_id, veiculo_id=uuid4(), motorista_id=uuid4(), data_hora_saida=base + timedelta(hours=1), data_hora_chegada_prevista=base + timedelta(hours=1, minutes=45), origem='Centro', destino='Viana')
    viagem_2.passageiros_embarcados = 100
    viagem_2.cancelar('Falha mecanica')
    await viagem_repo.save(viagem_2)
    viagem_3 = Viagem.programar(linha_id=viagem_1.linha_id, veiculo_id=uuid4(), motorista_id=uuid4(), data_hora_saida=base + timedelta(hours=2), data_hora_chegada_prevista=base + timedelta(hours=2, minutes=35), origem='Centro', destino='Viana')
    viagem_3.passageiros_embarcados = 140
    viagem_3.registrar_atraso(20)
    await viagem_repo.save(viagem_3)
    evento_1 = BilhetagemEletronica.registrar_evento(codigo_bilhete='BILH-A', viagem_id=viagem_1.id, tipo_tarifa=TipoTarifa.PUBLICA, valor_pago=Decimal('250.00'), forma_pagamento='cartao')
    evento_2 = BilhetagemEletronica.registrar_evento(codigo_bilhete='BILH-B', viagem_id=viagem_3.id, tipo_tarifa=TipoTarifa.PUBLICA, valor_pago=Decimal('300.00'), forma_pagamento='qrcode')
    await bilhetagem_repo.save(evento_1)
    await bilhetagem_repo.save(evento_2)
    demanda = await service.calcular_demanda(linha_id=viagem_1.linha_id, data_inicio=base - timedelta(minutes=5), data_fim=base + timedelta(hours=3))
    assert demanda.viagens_total == 3
    assert demanda.passageiros_total == 360
    assert demanda.passageiros_media_por_viagem == Decimal('120.00')
    assert demanda.arrecadacao_total == Decimal('550.00')
    qualidade = await service.calcular_qualidade(linha_id=viagem_1.linha_id, data_inicio=base - timedelta(minutes=5), data_fim=base + timedelta(hours=3))
    assert qualidade.viagens_total == 3
    assert qualidade.viagens_concluidas == 1
    assert qualidade.viagens_canceladas == 1
    assert qualidade.viagens_atrasadas == 1
    assert qualidade.pontualidade_percentual == Decimal('100.00')
    assert qualidade.taxa_cancelamento_percentual == Decimal('33.33')
    assert qualidade.taxa_atraso_percentual == Decimal('33.33')

def test_endpoint_analytics_demanda_retorna_200():
    demanda = SimpleNamespace(viagens_total=5, passageiros_total=650, passageiros_media_por_viagem=Decimal('130.00'), arrecadacao_total=Decimal('1500.00'))
    service = SimpleNamespace(calcular_demanda=AsyncMock(return_value=demanda))
    app = FastAPI()
    app.include_router(analytics_router, prefix='/transportes-logistica')
    app.dependency_overrides[get_operacao_analytics_service] = lambda: service
    client = TestClient(app)
    response = client.get('/transportes-logistica/analytics/demanda')
    assert response.status_code == 200
    assert response.json()['viagens_total'] == 5
