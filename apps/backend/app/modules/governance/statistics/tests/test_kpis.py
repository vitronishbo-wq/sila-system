from apps.backend.app.modules.governance.statistics.tests._fakes import kpi_payload, metrica_payload

def test_criar_kpi_e_performance(client):
    m_resp = client.post('/api/v1/estatistica/metricas/', json=metrica_payload())
    metrica_id = m_resp.json()['id']
    k_resp = client.post('/api/v1/estatistica/kpis/', json=kpi_payload(metrica_id))
    assert k_resp.status_code == 201
    kpi_id = k_resp.json()['id']
    up_resp = client.put(f'/api/v1/estatistica/kpis/{kpi_id}/valor', json={'valor': 60.0})
    assert up_resp.status_code == 200
    perf_resp = client.get(f'/api/v1/estatistica/kpis/{kpi_id}/performance')
    assert perf_resp.status_code == 200
    assert perf_resp.json()['performance'] > 0

def test_kpi_requer_metrica_existente(client):
    response = client.post('/api/v1/estatistica/kpis/', json=kpi_payload(999))
    assert response.status_code == 404