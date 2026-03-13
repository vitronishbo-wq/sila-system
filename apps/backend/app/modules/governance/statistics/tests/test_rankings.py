from app.modules.governance.statistics.tests._fakes import named_payload

def test_crud_rankings(client):
    create = client.post('/api/v1/estatistica/rankings/', json=named_payload('ranking-a'))
    assert create.status_code == 201
    entity_id = create.json()['id']
    listed = client.get('/api/v1/estatistica/rankings/')
    assert listed.status_code == 200
    assert listed.json()['total'] == 1
    detail = client.get(f'/api/v1/estatistica/rankings/{entity_id}')
    assert detail.status_code == 200
    patched = client.patch(f'/api/v1/estatistica/rankings/{entity_id}', json={'nome': 'ranking-b'})
    assert patched.status_code == 200
    deleted = client.delete(f'/api/v1/estatistica/rankings/{entity_id}')
    assert deleted.status_code == 204