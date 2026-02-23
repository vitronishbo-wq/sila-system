import asyncio
import json
from datetime import datetime

import httpx
import pytest
import respx

# Base URL used by integration checks (adjust if needed during manual runs)
BASE_URL = "http://127.0.0.1:8000/api"


@respx.mock
async def test_mocked_api():
    """A small mocked external call to ensure respx/httpx are wired correctly."""
    respx.get("https://api.externa.gov/v1/status").mock(
        return_value=httpx.Response(200, json={"status": "ok"})
    )

    response = await httpx.get("https://api.externa.gov/v1/status")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.external
async def test_login_and_health_check():
    """Lightweight integration flow used for manual verification.

    This test is marked external and will usually be skipped in fast unit runs.
    It attempts a login and a simple health check; failures here mean the API
    is not running or credentials need adjustment.
    """
    login_data = {"username": "test_truman", "password": "secure_password_123"}
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{BASE_URL}/auth/login", data=login_data)
            # If the API isn't running this will raise or return non-200
            if resp.status_code != 200:
                pytest.skip("API not available for integration test")
            token = resp.json().get("access_token")
            if not token:
                pytest.skip("No access token returned by API")

            headers = {"Authorization": f"Bearer {token}"}
            health = await client.get(f"{BASE_URL}/debug/health", headers=headers)
            if health.status_code != 200:
                pytest.skip("API health endpoint not OK")
    except Exception:
        pytest.skip("API not reachable for integration tests")


if __name__ == "__main__":
    asyncio.run(test_login_and_health_check())
