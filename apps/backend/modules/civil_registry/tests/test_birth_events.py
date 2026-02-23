import pytest
import uuid
from datetime import datetime

@pytest.mark.asyncio
async def test_register_birth_success(client, db_session):
    payload = {
        "nub": f"NUB-{uuid.uuid4().hex[:8]}",
        "full_name": "Junior dos Santos",
        "date_of_birth": "2026-02-01T10:00:00",
        "place_of_birth": "Luanda",
        "mother_name": "Maria dos Santos"
    }
    
    response = client.post("/api/v1/registo-civil/events/birth/", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["nub"] == payload["nub"]
    assert "citizen_id" in data

@pytest.mark.asyncio
async def test_register_birth_missing_data(client, db_session):
    payload = {
        "full_name": "Incompleto"
    }
    
    response = client.post("/api/v1/registo-civil/events/birth/", json=payload)
    
    # Depende de como o service trata, assumindo erro se faltar NUB
    assert response.status_code == 400
