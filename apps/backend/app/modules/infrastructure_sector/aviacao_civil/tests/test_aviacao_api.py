from __future__ import annotations
from datetime import datetime, timedelta
from uuid import uuid4
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.modules.infrastructure_sector.aviacao_civil.api.deps import reset_state_for_tests
from app.modules.infrastructure_sector.aviacao_civil.api.router import router
app = FastAPI()
app.include_router(router, prefix='/v1')
client = TestClient(app)

def setup_function() -> None:
    import asyncio
    asyncio.run(reset_state_for_tests())

def test_fluxo_basico_api_aviacao() -> None:
    aeronave_payload = {'matricula': 'D2-XYZ', 'tipo': 'aviao', 'categoria': 'transporte_passageiro', 'fabricante': 'Airbus', 'modelo': 'A320', 'numero_serie': 'A320-SN1', 'ano_fabricacao': 2019, 'proprietario_cpf_cnpj': '50010020030', 'capacidade_passageiros': 180, 'autonomia_km': 6100, 'peso_maximo_decolagem_kg': 77000}
    aeronave_resp = client.post('/v1/aviacao-civil/aeronaves/', json=aeronave_payload)
    assert aeronave_resp.status_code == 201, aeronave_resp.text
    aeronave_id = aeronave_resp.json()['id']
    partida = datetime.utcnow() + timedelta(hours=3)
    chegada = partida + timedelta(hours=1, minutes=10)
    voo_payload = {'numero_voo': 'DT2002', 'empresa_id': str(uuid4()), 'aeronave_id': aeronave_id, 'aeroporto_origem_id': str(uuid4()), 'aeroporto_destino_id': str(uuid4()), 'data_hora_partida': partida.isoformat(), 'data_hora_chegada': chegada.isoformat(), 'tipo': 'regular', 'natureza': 'domestico', 'regras': 'ifr', 'passageiros': 95, 'tripulantes': [{'funcao': 'piloto', 'nome': 'Cmd B'}]}
    voo_resp = client.post('/v1/aviacao-civil/voos/', json=voo_payload)
    assert voo_resp.status_code == 201, voo_resp.text
    voo_id = voo_resp.json()['id']
    decolagem_resp = client.post(f'/v1/aviacao-civil/voos/{voo_id}/decolagem', json={'data_hora': (partida + timedelta(minutes=5)).isoformat()})
    assert decolagem_resp.status_code == 200
    assert decolagem_resp.json()['status'] == 'em_voo'
    pouso_resp = client.post(f'/v1/aviacao-civil/voos/{voo_id}/pouso', json={'data_hora': (partida + timedelta(hours=1, minutes=18)).isoformat()})
    assert pouso_resp.status_code == 200
    assert pouso_resp.json()['status'] == 'pousado'

def test_ocorrencia_api() -> None:
    payload = {'tipo': 'incidente', 'aeronave_id': str(uuid4()), 'data_ocorrencia': datetime.utcnow().isoformat(), 'local': {'latitude': -8.84, 'longitude': 13.23}, 'fase_voo': 'aproximacao', 'descricao': 'Bird strike sem danos estruturais relevantes', 'vitimas': {'fatais': 0, 'graves': 0, 'leves': 0}, 'danos': 'LEVE'}
    response = client.post('/v1/aviacao-civil/ocorrencias/', json=payload)
    assert response.status_code == 201, response.text
    assert response.json()['gravidade'] in {'leve', 'moderada', 'grave', 'fatal'}