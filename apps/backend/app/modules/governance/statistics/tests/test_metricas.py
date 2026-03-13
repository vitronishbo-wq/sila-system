from apps.backend.app.modules.governance.statistics.tests._fakes import metrica_payload

def test_criar_obter_listar_metrica(client):
    response = client.post('/api/v1/estatistica/metricas/', json=metrica_payload())
    assert response.status_code == 201
    created = response.json()
    get_resp = client.get(f'/api/v1/estatistica/metricas/{created['id']}')
    assert get_resp.status_code == 200
    assert get_resp.json()['nome'] == 'taxa_emprego'
    list_resp = client.get('/api/v1/estatistica/metricas/')
    assert list_resp.status_code == 200
    assert list_resp.json()['total'] == 1

def test_atualizar_valor_metrica(client):
    response = client.post('/api/v1/estatistica/metricas/', json=metrica_payload())
    metrica_id = response.json()['id']
    up_resp = client.put(f'/api/v1/estatistica/metricas/{metrica_id}/valor', json={'valor': 95.0})
    assert up_resp.status_code == 200
    assert up_resp.json()['valor_atual'] == 95.0