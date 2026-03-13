from app.modules.governance.statistics.tests._fakes import named_payload

def test_crud_analises(client):
    create = client.post('/api/v1/estatistica/analises/', json=named_payload('analise-a'))
    assert create.status_code == 201
    entity_id = create.json()['id']
    listed = client.get('/api/v1/estatistica/analises/')
    assert listed.status_code == 200
    assert listed.json()['total'] == 1
    detail = client.get(f'/api/v1/estatistica/analises/{entity_id}')
    assert detail.status_code == 200
    patched = client.patch(f'/api/v1/estatistica/analises/{entity_id}', json={'nome': 'analise-b'})
    assert patched.status_code == 200
    deleted = client.delete(f'/api/v1/estatistica/analises/{entity_id}')
    assert deleted.status_code == 204