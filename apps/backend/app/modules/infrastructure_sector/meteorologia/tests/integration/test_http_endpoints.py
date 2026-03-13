from __future__ import annotations
from datetime import datetime, timezone
from uuid import UUID, uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.modules.infrastructure_sector.meteorologia.api.deps import get_estacao_service, get_processamento_service
from app.modules.infrastructure_sector.meteorologia.api.router import router as meteorologia_router
from app.modules.infrastructure_sector.meteorologia.domain.enums import StationStatus
from app.modules.infrastructure_sector.meteorologia.domain.models import EstacaoMeteorologica, ObservacaoMeteorologica

class FakeEstacaoService:

    def __init__(self) -> None:
        self._estacoes: dict[UUID, EstacaoMeteorologica] = {}

    async def criar_estacao(self, payload: dict) -> EstacaoMeteorologica:
        codigo = str(payload['codigo']).strip().upper()
        if any((e.codigo == codigo for e in self._estacoes.values())):
            raise ValueError(f'Ja existe estacao com codigo {codigo}')
        estacao = EstacaoMeteorologica(codigo=codigo, nome=payload['nome'], latitude=payload['latitude'], longitude=payload['longitude'], altitude=payload.get('altitude'), municipio=payload.get('municipio'), provincia=payload.get('provincia'), metadata=payload.get('metadata') or {}, status=StationStatus.ACTIVE)
        self._estacoes[estacao.id] = estacao
        return estacao

    async def listar_estacoes(self, *, provincia: str | None=None, status: str | None=None, limit: int=100, offset: int=0) -> list[EstacaoMeteorologica]:
        result = list(self._estacoes.values())
        if provincia:
            result = [e for e in result if e.provincia == provincia]
        if status:
            status_enum = StationStatus(status.upper())
            result = [e for e in result if e.status == status_enum]
        return result[offset:offset + limit]

    async def obter_estacao(self, estacao_id: UUID) -> EstacaoMeteorologica:
        estacao = self._estacoes.get(estacao_id)
        if estacao is None:
            raise ValueError('Estacao nao encontrada')
        return estacao

    async def atualizar_estacao(self, estacao_id: UUID, payload: dict) -> EstacaoMeteorologica:
        estacao = await self.obter_estacao(estacao_id)
        if 'nome' in payload and payload['nome'] is not None:
            estacao.nome = payload['nome']
        if 'municipio' in payload and payload['municipio'] is not None:
            estacao.municipio = payload['municipio']
        if 'provincia' in payload and payload['provincia'] is not None:
            estacao.provincia = payload['provincia']
        if 'status' in payload and payload['status'] is not None:
            estacao.status = StationStatus(str(payload['status']).upper())
        if 'metadata' in payload and payload['metadata'] is not None:
            estacao.metadata = payload['metadata']
        if any((key in payload and payload[key] is not None for key in ('latitude', 'longitude', 'altitude'))):
            latitude = payload.get('latitude', estacao.latitude)
            longitude = payload.get('longitude', estacao.longitude)
            altitude = payload.get('altitude', estacao.altitude)
            if latitude is None or longitude is None:
                raise ValueError('Latitude e longitude sao obrigatorias para atualizar localizacao')
            estacao.update_location(latitude=latitude, longitude=longitude, altitude=altitude)
        estacao.updated_at = datetime.now(timezone.utc)
        return estacao

    async def remover_estacao(self, estacao_id: UUID) -> None:
        if estacao_id not in self._estacoes:
            raise ValueError('Estacao nao encontrada')
        del self._estacoes[estacao_id]

class FakeProcessamentoService:

    def __init__(self, estacao_service: FakeEstacaoService) -> None:
        self._estacao_service = estacao_service
        self._observacoes: dict[UUID, ObservacaoMeteorologica] = {}

    async def processar_observacao(self, observacao: ObservacaoMeteorologica) -> dict:
        if observacao.estacao_id not in self._estacao_service._estacoes:
            return {'sucesso': False, 'observacao_id': str(observacao.id), 'alertas_gerados': 0, 'warnings': [], 'erros': [f'Estacao {observacao.estacao_id} nao encontrada'], 'observacao': None}
        observacao.analisar_severidade()
        self._observacoes[observacao.id] = observacao
        return {'sucesso': True, 'observacao_id': str(observacao.id), 'alertas_gerados': len(observacao.alerts), 'warnings': [], 'erros': [], 'observacao': observacao}

    async def obter_observacao(self, observacao_id: UUID) -> ObservacaoMeteorologica:
        observacao = self._observacoes.get(observacao_id)
        if observacao is None:
            raise ValueError('Observacao nao encontrada')
        return observacao

    async def listar_observacoes_estacao(self, *, estacao_id: UUID, start_date: datetime | None=None, end_date: datetime | None=None, limit: int=100) -> list[ObservacaoMeteorologica]:
        result = [o for o in self._observacoes.values() if o.estacao_id == estacao_id]
        if start_date:
            result = [o for o in result if o.data_observacao >= start_date]
        if end_date:
            result = [o for o in result if o.data_observacao <= end_date]
        result.sort(key=lambda o: o.data_observacao, reverse=True)
        return result[:limit]

    async def listar_observacoes_com_alertas(self, *, start_date: datetime | None=None, end_date: datetime | None=None, limit: int=50) -> list[ObservacaoMeteorologica]:
        result = [o for o in self._observacoes.values() if o.has_alerts]
        if start_date:
            result = [o for o in result if o.data_observacao >= start_date]
        if end_date:
            result = [o for o in result if o.data_observacao <= end_date]
        result.sort(key=lambda o: o.data_observacao, reverse=True)
        return result[:limit]

@pytest.fixture
def http_client() -> TestClient:
    app = FastAPI()
    app.include_router(meteorologia_router, prefix='/api/v1')
    estacao_service = FakeEstacaoService()
    processamento_service = FakeProcessamentoService(estacao_service)
    app.dependency_overrides[get_estacao_service] = lambda: estacao_service
    app.dependency_overrides[get_processamento_service] = lambda: processamento_service
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()

def _criar_estacao_base(client: TestClient, codigo: str='ST-LDA-001') -> dict:
    response = client.post('/api/v1/meteorologia/estacoes/', json={'codigo': codigo, 'nome': 'Estacao Central', 'latitude': -8.8383, 'longitude': 13.2344, 'altitude': 74.0, 'municipio': 'Luanda', 'provincia': 'Luanda'})
    assert response.status_code == 201, response.text
    return response.json()

def test_estacoes_criar_listar_filtrar(http_client: TestClient) -> None:
    _criar_estacao_base(http_client, codigo='ST-LDA-101')
    _criar_estacao_base(http_client, codigo='ST-HBO-201')
    response = http_client.get('/api/v1/meteorologia/estacoes/?provincia=Luanda&status=ACTIVE')
    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 2
    assert all((item['status'] == 'ACTIVE' for item in payload))

def test_estacoes_obter_atualizar_remover_fluxo(http_client: TestClient) -> None:
    created = _criar_estacao_base(http_client, codigo='ST-UPD-001')
    estacao_id = created['id']
    get_response = http_client.get(f'/api/v1/meteorologia/estacoes/{estacao_id}')
    assert get_response.status_code == 200
    assert get_response.json()['codigo'] == 'ST-UPD-001'
    put_response = http_client.put(f'/api/v1/meteorologia/estacoes/{estacao_id}', json={'nome': 'Estacao Atualizada', 'status': 'MAINTENANCE'})
    assert put_response.status_code == 200
    assert put_response.json()['nome'] == 'Estacao Atualizada'
    assert put_response.json()['status'] == 'MAINTENANCE'
    delete_response = http_client.delete(f'/api/v1/meteorologia/estacoes/{estacao_id}')
    assert delete_response.status_code == 204
    get_after_delete = http_client.get(f'/api/v1/meteorologia/estacoes/{estacao_id}')
    assert get_after_delete.status_code == 404

def test_observacoes_criar_obter_e_listar_alertas(http_client: TestClient) -> None:
    estacao = _criar_estacao_base(http_client, codigo='ST-OBS-001')
    post_response = http_client.post('/api/v1/meteorologia/observacoes/', json={'estacao_id': estacao['id'], 'temperatura': 44.2, 'humidade': 12.0, 'velocidade_vento': 90.0, 'tipo': 'SURFACE'})
    assert post_response.status_code == 201, post_response.text
    created = post_response.json()
    assert created['has_alerts'] is True
    assert len(created['alertas']) >= 2
    observacao_id = created['id']
    get_response = http_client.get(f'/api/v1/meteorologia/observacoes/{observacao_id}')
    assert get_response.status_code == 200
    assert get_response.json()['id'] == observacao_id
    alertas_response = http_client.get('/api/v1/meteorologia/observacoes/alertas/recentes')
    assert alertas_response.status_code == 200
    alertas_payload = alertas_response.json()
    assert len(alertas_payload) >= 1
    assert alertas_payload[0]['has_alerts'] is True

def test_observacoes_listar_por_estacao_e_validar_erro_estacao_inexistente(http_client: TestClient) -> None:
    estacao = _criar_estacao_base(http_client, codigo='ST-OBS-002')
    estacao_id = estacao['id']
    response_a = http_client.post('/api/v1/meteorologia/observacoes/', json={'estacao_id': estacao_id, 'temperatura': 30.0, 'humidade': 60.0, 'tipo': 'SURFACE'})
    assert response_a.status_code == 201
    response_b = http_client.post('/api/v1/meteorologia/observacoes/', json={'estacao_id': estacao_id, 'temperatura': 41.0, 'humidade': 18.0, 'tipo': 'SURFACE'})
    assert response_b.status_code == 201
    list_response = http_client.get(f'/api/v1/meteorologia/observacoes/estacao/{estacao_id}?limit=10')
    assert list_response.status_code == 200
    payload = list_response.json()
    assert len(payload) == 2
    invalid_response = http_client.post('/api/v1/meteorologia/observacoes/', json={'estacao_id': str(uuid4()), 'temperatura': 29.0, 'humidade': 40.0, 'tipo': 'SURFACE'})
    assert invalid_response.status_code == 400
    detail = invalid_response.json()['detail']
    assert 'erros' in detail
    assert 'nao encontrada' in detail['erros'][0].lower()