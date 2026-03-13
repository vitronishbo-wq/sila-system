from app.modules.governance.statistics.tests._fakes import kpi_payload, metrica_payload

def test_fluxo_basico_metrica_kpi_dashboard(client):
    metrica = client.post('/api/v1/estatistica/metricas/', json=metrica_payload()).json()
    kpi_resp = client.post('/api/v1/estatistica/kpis/', json=kpi_payload(metrica['id']))
    assert kpi_resp.status_code == 201
    kpi = kpi_resp.json()
    update_resp = client.put(f'/api/v1/estatistica/kpis/{kpi['id']}/valor', json={'valor': 55.0})
    assert update_resp.status_code == 200
    dash_resp = client.post('/api/v1/estatistica/dashboards/', json={'nome': 'exec', 'tipo': 'executivo', 'kpi_ids': [kpi['id']]})
    assert dash_resp.status_code == 201