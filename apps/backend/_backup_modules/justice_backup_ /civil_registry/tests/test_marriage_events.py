import pytest

@pytest.mark.asyncio
async def test_register_marriage_success(client, db_session):
    payload = {'spouse1_id': 'FUC-123', 'spouse2_id': 'FUC-456', 'marriage_date': '2026-02-09T14:00:00', 'regime': 'comunhao_adquiridos', 'place_of_marriage': 'Conservatória de Luanda'}
    response = client.post('/api/v1/registo-civil/events/marriage/', json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert 'marriage_id' in data

@pytest.mark.asyncio
async def test_register_marriage_invalid_regime(client, db_session):
    payload = {'spouse1_id': 'FUC-1', 'spouse2_id': 'FUC-2', 'marriage_date': '2026-02-09T14:00:00', 'regime': 'INVALIDO'}
    response = client.post('/api/v1/registo-civil/events/marriage/', json=payload)
    assert response.status_code == 400