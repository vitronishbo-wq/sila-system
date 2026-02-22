from fastapi import status

# Fluxo simplificado: criar cidadão -> simular processo -> associar pagamento


def test_health_module_integration(client):
    """Test health module endpoints that are actually implemented."""
    # Test health ping endpoint
    r = client.get("/health/ping")
    assert r.status_code == 200

    # Test creating a health record
    health_payload = {"patient_name": "Test Patient", "diagnosis": "Test"}
    r = client.post("/health/", json=health_payload)
    assert r.status_code in (200, 201)

    # Test getting health records
    r = client.get("/health/")
    assert r.status_code == 200
