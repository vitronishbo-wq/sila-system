from app.modules.governance.statistics.tests._fakes import named_payload

def test_crud_tendencias(client):
    create = client.post('/api/v1/estatistica/tendencias/', json=named_payload('tendencia-a'))
    assert create.status_code == 201
    entity_id = create.json()['id']
    listed = client.get('/api/v1/estatistica/tendencias/')
    assert listed.status_code == 200
    assert listed.json()['total'] == 1
    detail = client.get(f'/api/v1/estatistica/tendencias/{entity_id}')
    assert detail.status_code == 200
    patched = client.patch(f'/api/v1/estatistica/tendencias/{entity_id}', json={'nome': 'tendencia-b'})
    assert patched.status_code == 200
    deleted = client.delete(f'/api/v1/estatistica/tendencias/{entity_id}')
    assert deleted.status_code == 204