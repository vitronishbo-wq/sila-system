"""Test health endpoints directly."""

import requests


def test_health_check():
    """Test GET /health/ endpoint."""
    base_url = "http://localhost:8000"
    response = requests.get(f"{base_url}/health/")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert "status" in response.json(), "Response JSON missing 'status' key"


def test_health_metrics():
    """Test GET /health/metrics endpoint."""
    base_url = "http://localhost:8000"
    response = requests.get(f"{base_url}/health/metrics")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert "metrics" in response.json(), "Response JSON missing 'metrics' key"
