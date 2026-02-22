import pytest

@pytest.mark.asyncio
async def test_register_death_success(client, db_session):
    payload = {
        "citizen_id": "FUC-DECEASED-1",
        "death_date": "2026-02-09T08:00:00",
        "place_of_death": "Hospital Central",
        "cause_of_death": "Causas Naturais"
    }
    
    response = client.post("/api/v1/registo-civil/events/death/", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "death_certificate_id" in data
