from __future__ import annotations
import asyncio
from datetime import date, timedelta
from uuid import uuid4
from fastapi import FastAPI
from fastapi.testclient import TestClient
from apps.backend.app.modules.governance.cooperacao_internacional.api.deps import reset_state_for_tests
from apps.backend.app.modules.governance.cooperacao_internacional.api.router import router
app = FastAPI()
app.include_router(router, prefix='/v1')
client = TestClient(app)

def setup_function() -> None:
    asyncio.run(reset_state_for_tests())

def test_fluxo_api_acordo_projeto_visto() -> None:
    acordo_payload = {'titulo': 'Tratado de Mobilidade Academica', 'tipo': 'tratado', 'natureza': 'vinculante', 'data_assinatura': date.today().isoformat(), 'data_vigor': None, 'prazo_anos': 4, 'objeto': 'Mobilidade de docentes e estudantes entre universidades parceiras'}
    acordo_resp = client.post('/v1/cooperacao-internacional/acordos/', json=acordo_payload)
    assert acordo_resp.status_code == 201, acordo_resp.text
    acordo_id = acordo_resp.json()['id']
    assinar_resp = client.post(f'/v1/cooperacao-internacional/acordos/{acordo_id}/assinar', json={'local_assinatura': 'Luanda', 'partes': [{'entidade_id': str(uuid4()), 'tipo_entidade': 'PAIS', 'data_adesao': date.today().isoformat(), 'assinante': 'Ministro A', 'titulo_assinante': 'Ministro'}]})
    assert assinar_resp.status_code == 200, assinar_resp.text
    assert assinar_resp.json()['status'] == 'assinado'
    projeto_resp = client.post('/v1/cooperacao-internacional/projetos/', json={'titulo': 'Projeto de Capacitacao Diplomatica', 'tipo': 'cooperacao_tecnica', 'modalidade': 'bilateral', 'acordo_base_id': acordo_id, 'orgao_responsavel_id': str(uuid4()), 'orgao_parceiro_id': str(uuid4()), 'pais_parceiro_id': str(uuid4()), 'data_inicio': date.today().isoformat(), 'data_fim': (date.today() + timedelta(days=180)).isoformat(), 'objetivo_geral': 'Formacao de tecnicos para negociacao internacional', 'objetivos_especificos': ['Treinamento', 'Intercambio'], 'orcamento_total': 150000.0, 'fonte_recursos': 'Cooperacao bilateral'})
    assert projeto_resp.status_code == 201, projeto_resp.text
    visto_resp = client.post('/v1/cooperacao-internacional/vistos/', json={'tipo': 'oficial', 'categoria': 'vitem_ii', 'solicitante_cpf': '12345678900', 'solicitante_nome': 'Representante Oficial', 'solicitante_passaporte': 'P998877', 'pais_origem_id': str(uuid4()), 'pais_destino_id': str(uuid4()), 'data_entrada_prevista': date.today().isoformat(), 'data_saida_prevista': (date.today() + timedelta(days=30)).isoformat(), 'objetivo_viagem': 'Negociacao de acordo de cooperacao', 'consulato_emissor_id': str(uuid4())})
    assert visto_resp.status_code == 201, visto_resp.text
    visto_id = visto_resp.json()['id']
    aprovar_resp = client.post(f'/v1/cooperacao-internacional/vistos/{visto_id}/aprovar', json={'autoridade': 'Consul Geral', 'validade_dias': 180})
    assert aprovar_resp.status_code == 200, aprovar_resp.text
    assert aprovar_resp.json()['status'] == 'aprovado'
    emitir_resp = client.post(f'/v1/cooperacao-internacional/vistos/{visto_id}/emitir')
    assert emitir_resp.status_code == 200, emitir_resp.text
    assert emitir_resp.json()['status'] == 'emitido'