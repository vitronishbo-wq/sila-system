def test_criar_listar_dashboard(client):
    data = {'nome': 'dashboard executivo', 'descricao': 'visao gerencial', 'tipo': 'executivo', 'kpi_ids': []}
    create_resp = client.post('/api/v1/estatistica/dashboards/', json=data)
    assert create_resp.status_code == 201
    list_resp = client.get('/api/v1/estatistica/dashboards/')
    assert list_resp.status_code == 200
    assert list_resp.json()['total'] == 1