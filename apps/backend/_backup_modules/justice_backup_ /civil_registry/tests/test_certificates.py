import pytest

@pytest.mark.asyncio
async def test_issue_birth_certificate(client, db_session):
    response = client.get('/api/v1/registo-civil/certificates/birth/FUC-ANY')
    assert response.status_code == 200
    assert response.json()['type'] == 'BIRTH'

@pytest.mark.asyncio
async def test_issue_marriage_certificate(client, db_session):
    response = client.get('/api/v1/registo-civil/certificates/marriage/MAR-123')
    assert response.status_code == 200
    assert response.json()['type'] == 'MARRIAGE'

@pytest.mark.asyncio
async def test_issue_civil_state_certificate(client, db_session):
    response = client.get('/api/v1/registo-civil/certificates/civil-state/FUC-ANY')
    assert response.status_code == 200
    assert response.json()['type'] == 'CIVIL_STATE'