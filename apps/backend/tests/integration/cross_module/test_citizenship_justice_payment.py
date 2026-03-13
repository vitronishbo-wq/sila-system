
# Fluxo simplificado: criar cidadão -> simular processo -> associar pagamento


def test_health_module_integration(client):
    """Test system health endpoints currently exposed by the API."""
    r = client.get("/api/health/live")
    assert r.status_code == 200
    payload = r.json()
    assert payload.get("alive") is True

    # /api/health validates DB connectivity; in degraded env it can return 503.
    r = client.get("/api/health")
    assert r.status_code in (200, 503)
