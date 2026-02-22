import pytest

pytest.importorskip("backend.main")

from apps.backend.main import app
from httpx import AsyncClient


@pytest.mark.asyncio
class TestAuthFlow:

    @pytest.fixture(scope="module")
    async def async_client(self):
        async with AsyncClient(app=app, base_url="http://testserver") as client:
            yield client

    async def test_user_login(self, async_client):
        # Example test for user login
        response = await async_client.post(
            "/auth/login", json={"username": "testuser", "password": "password123"}
        )
        assert response.status_code == 200
        assert "access_token" in response.json()

    async def test_refresh_token(self, async_client):
        # Example test for refreshing token
        login_response = await async_client.post(
            "/auth/login", json={"username": "testuser", "password": "password123"}
        )
        refresh_token = login_response.json().get("refresh_token")

        response = await async_client.post(
            "/auth/refresh", json={"refresh_token": refresh_token}
        )
        assert response.status_code == 200
        assert "access_token" in response.json()

    async def test_protected_route_access(self, async_client):
        # Example test for accessing a protected route
        login_response = await async_client.post(
            "/auth/login", json={"username": "testuser", "password": "password123"}
        )
        access_token = login_response.json().get("access_token")

        headers = {"Authorization": f"Bearer {access_token}"}
        response = await async_client.get("/protected-route", headers=headers)
        assert response.status_code == 200
