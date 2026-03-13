from __future__ import annotations
from types import SimpleNamespace
from uuid import uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.modules.resources.florestas.api.deps import get_estatistica_florestal_service
from app.modules.resources.florestas.api.router import router as florestas_router
from app.modules.resources.florestas.api import deps as florestas_deps
from app.modules.resources.florestas.application.services.estatistica_florestal_service import EstatisticaFlorestalService
from app.modules.resources.florestas.infrastructure.adapters.agricultura_service_adapter import AgriculturaServiceAdapter
from app.modules.resources.florestas.infrastructure.adapters.ambiente_service_adapter import AmbienteServiceAdapter
from app.modules.resources.florestas.infrastructure.adapters.comercio_externo_service_adapter import ComercioExternoServiceAdapter
from app.modules.resources.florestas.infrastructure.adapters.energia_service_adapter import EnergiaServiceAdapter
from app.modules.resources.florestas.infrastructure.adapters.geosampa_service_adapter import GeosampaServiceAdapter
from app.modules.resources.florestas.infrastructure.adapters.gestao_fundiaria_service_adapter import GestaoFundiariaServiceAdapter

class _OperadorRepo:

    def __init__(self, operadores):
        self._operadores = operadores

    async def list_all(self, ativo=None):
        return self._operadores

class _UnidadeRepo:

    def __init__(self, mapping):
        self._mapping = mapping

    async def list_by_operador(self, operador_id):
        return self._mapping.get(operador_id, [])

class _PlanoRepo:

    def __init__(self, mapping):
        self._mapping = mapping

    async def list_by_unidade(self, unidade_id):
        return self._mapping.get(unidade_id, [])

class _InventarioRepo:

    def __init__(self, mapping):
        self._mapping = mapping

    async def list_by_unidade(self, unidade_id):
        return self._mapping.get(unidade_id, [])

class _ExternalOk:

    async def available(self) -> bool:
        return True

    async def integration_payload(self) -> dict[str, str]:
        return {'status': 'ok'}

class _ExternalDown:

    async def available(self) -> bool:
        return False

    async def integration_payload(self) -> dict[str, str]:
        return {'status': 'down'}

class _FakeEstatisticaService:

    async def gerar_dashboard(self):
        return {'operacional': {'total_operadores': 3, 'total_unidades_manejo': 6, 'total_planos_manejo': 4, 'total_inventarios': 9, 'media_unidades_por_operador': 2.0, 'media_planos_por_unidade': 0.67}, 'integracao': {'integracao_ok': True, 'modulos_ativos': 6, 'modulos_totais': 6, 'modulos': [{'modulo': 'ambiente', 'available': True, 'detalhes': {'status': 'ok'}}]}}

    async def gerar_resumo_operacional(self):
        return (await self.gerar_dashboard())['operacional']

    async def gerar_status_integracao(self):
        return (await self.gerar_dashboard())['integracao']

class _DummyListService:

    async def listar(self, *args, **kwargs):
        return []

class _DummyGeracaoService:

    async def get_visao_consolidada(self):
        return {'centrais': [], 'subestacoes': [], 'linhas': [], 'errors': {}, 'degraded': False}

@pytest.fixture
def api_client():
    app = FastAPI()
    app.include_router(florestas_router, prefix='/v1')

    async def _override():
        return _FakeEstatisticaService()
    app.dependency_overrides[get_estatistica_florestal_service] = _override
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_resumo_operacional_agrega_metricas():
    op1, op2 = (uuid4(), uuid4())
    um1, um2, um3 = (uuid4(), uuid4(), uuid4())
    service = EstatisticaFlorestalService(operador_repo=_OperadorRepo([SimpleNamespace(id=op1), SimpleNamespace(id=op2)]), unidade_repo=_UnidadeRepo({op1: [SimpleNamespace(id=um1), SimpleNamespace(id=um2)], op2: [SimpleNamespace(id=um3)]}), plano_repo=_PlanoRepo({um1: [1], um2: [1, 2], um3: []}), inventario_repo=_InventarioRepo({um1: [1], um2: [1], um3: [1, 2, 3]}), ambiente_service=_ExternalOk(), gestao_fundiaria_service=_ExternalOk(), agricultura_service=_ExternalOk(), energia_service=_ExternalOk(), comercio_externo_service=_ExternalOk(), geosampa_service=_ExternalOk())
    resumo = await service.gerar_resumo_operacional()
    assert resumo['total_operadores'] == 2
    assert resumo['total_unidades_manejo'] == 3
    assert resumo['total_planos_manejo'] == 3
    assert resumo['total_inventarios'] == 5
    assert resumo['media_unidades_por_operador'] == 1.5
    assert resumo['media_planos_por_unidade'] == 1.0

@pytest.mark.asyncio
async def test_status_integracao_identifica_modulo_indisponivel():
    service = EstatisticaFlorestalService(operador_repo=_OperadorRepo([]), unidade_repo=_UnidadeRepo({}), plano_repo=_PlanoRepo({}), inventario_repo=_InventarioRepo({}), ambiente_service=_ExternalOk(), gestao_fundiaria_service=_ExternalDown(), agricultura_service=_ExternalOk(), energia_service=_ExternalOk(), comercio_externo_service=_ExternalOk(), geosampa_service=_ExternalOk())
    status = await service.gerar_status_integracao()
    assert status['integracao_ok'] is False
    assert status['modulos_totais'] == 6
    assert status['modulos_ativos'] == 5

def test_api_dashboard_estatistico(api_client: TestClient):
    response = api_client.get('/v1/florestas/estatisticas-florestais/')
    assert response.status_code == 200
    body = response.json()
    assert body['operacional']['total_operadores'] == 3
    assert body['integracao']['integracao_ok'] is True

def test_api_resumo_operacional(api_client: TestClient):
    response = api_client.get('/v1/florestas/estatisticas-florestais/operacional')
    assert response.status_code == 200
    body = response.json()
    assert body['total_unidades_manejo'] == 6
    assert body['media_unidades_por_operador'] == 2.0

def test_api_relatorio_integracao(api_client: TestClient):
    response = api_client.get('/v1/florestas/estatisticas-florestais/relatorios/integracao')
    assert response.status_code == 200
    body = response.json()
    assert body['modulos_totais'] == 6
    assert body['modulos_ativos'] == 6

@pytest.mark.asyncio
async def test_deps_conecta_adapters_com_servicos_reais(monkeypatch):
    monkeypatch.setattr(florestas_deps, 'get_cadastro_service', lambda: _DummyListService())
    monkeypatch.setattr(florestas_deps, 'get_imovel_service', lambda: _DummyListService())
    monkeypatch.setattr(florestas_deps, 'get_propriedade_service', lambda: _DummyListService())
    monkeypatch.setattr(florestas_deps, 'get_geracao_service', lambda: _DummyGeracaoService())

    async def _get_exportador_service(_session):
        return _DummyListService()
    monkeypatch.setattr(florestas_deps, 'get_exportador_service', _get_exportador_service)
    service = await florestas_deps.get_estatistica_florestal_service(session=object())
    status = await service.gerar_status_integracao()
    assert status['integracao_ok'] is True
    assert status['modulos_totais'] == 6

class _ListDependency:

    def __init__(self, size: int=0):
        self._size = size

    async def listar(self, *args, **kwargs):
        return [object() for _ in range(self._size)]

class _EnergyDependency:

    async def get_visao_consolidada(self):
        return {'centrais': [1, 2], 'subestacoes': [1], 'linhas': [1, 2, 3], 'errors': {}, 'degraded': False}

class _GeoDependency:

    async def get_all_provinces(self, *args, **kwargs):
        return []

@pytest.mark.asyncio
@pytest.mark.parametrize(('adapter', 'expected_capability', 'metric_key', 'metric_value'), [(AmbienteServiceAdapter(_ListDependency(3)), 'licenciamento_ambiental', 'car_registrados', 3), (GestaoFundiariaServiceAdapter(_ListDependency(4)), 'cadastro_imoveis_car', 'imoveis_registrados', 4), (AgriculturaServiceAdapter(_ListDependency(5)), 'correlacao_uso_solo', 'propriedades_rurais', 5), (ComercioExternoServiceAdapter(_ListDependency(6)), 'controle_exportacao_madeira', 'exportadores_habilitados', 6)])
async def test_contract_payload_integracao_lista(adapter, expected_capability, metric_key, metric_value):
    assert await adapter.available() is True
    payload = await adapter.integration_payload()
    assert isinstance(payload, dict)
    assert isinstance(payload.get('provider'), str)
    assert payload.get('capability') == expected_capability
    assert payload.get(metric_key) == metric_value

@pytest.mark.asyncio
async def test_contract_payload_integracao_energia():
    adapter = EnergiaServiceAdapter(_EnergyDependency())
    assert await adapter.available() is True
    payload = await adapter.integration_payload()
    assert isinstance(payload, dict)
    assert payload.get('capability') == 'restricoes_infraestrutura_energetica'
    assert payload.get('centrais') == 2
    assert payload.get('subestacoes') == 1
    assert payload.get('linhas_transmissao') == 3

@pytest.mark.asyncio
async def test_contract_payload_integracao_geosampa():
    adapter = GeosampaServiceAdapter(_GeoDependency())
    assert await adapter.available() is True
    payload = await adapter.integration_payload()
    assert isinstance(payload, dict)
    assert payload.get('capability') == 'base_geoespacial'
    assert payload.get('supports_provincias') is True

@pytest.mark.asyncio
@pytest.mark.parametrize('adapter', [AmbienteServiceAdapter(None), GestaoFundiariaServiceAdapter(None), AgriculturaServiceAdapter(None), ComercioExternoServiceAdapter(None)])
async def test_contract_payload_integracao_sem_dependencia_lista(adapter):
    assert await adapter.available() is False
    payload = await adapter.integration_payload()
    assert payload['provider'] == 'none'
    assert isinstance(payload['capability'], str)

@pytest.mark.asyncio
async def test_contract_payload_integracao_energia_sem_dependencia():
    adapter = EnergiaServiceAdapter(None)
    assert await adapter.available() is False
    payload = await adapter.integration_payload()
    assert payload['provider'] == 'none'
    assert payload['centrais'] is None
    assert payload['subestacoes'] is None
    assert payload['linhas_transmissao'] is None

@pytest.mark.asyncio
async def test_contract_payload_integracao_geosampa_sem_dependencia():
    adapter = GeosampaServiceAdapter(None)
    assert await adapter.available() is False
    payload = await adapter.integration_payload()
    assert payload['provider'] == 'none'
    assert payload['supports_provincias'] is False