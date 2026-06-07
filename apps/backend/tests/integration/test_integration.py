import pytest

pytest.importorskip("backend.main")

from httpx import AsyncClient

from apps.backend.main import app


@pytest.mark.asyncio
class TestIntegration:
    @pytest.fixture(scope="module")
    async def async_client(self):
        async with AsyncClient(app=app, base_url="http://testserver") as client:
            yield client

    async def test_end_to_end_flow(self, async_client):
        # Step 1: Create a user
        create_response = await async_client.post(
            "/users/", json={"username": "testuser", "password": "password123"}
        )
        assert create_response.status_code == 201
        user_id = create_response.json().get("id")

        # Step 2: Log in
        login_response = await async_client.post(
            "/auth/login", json={"username": "testuser", "password": "password123"}
        )
        assert login_response.status_code == 200
        access_token = login_response.json().get("access_token")

        # Step 3: Access a protected route
        headers = {"Authorization": f"Bearer {access_token}"}
        protected_response = await async_client.get("/protected-route", headers=headers)
        assert protected_response.status_code == 200

        # Step 4: Update user data
        update_response = await async_client.put(
            f"/users/{user_id}", json={"username": "updateduser"}, headers=headers
        )
        assert update_response.status_code == 200
        assert update_response.json().get("username") == "updateduser"

        # Step 5: Delete the user
        delete_response = await async_client.delete(f"/users/{user_id}", headers=headers)
        assert delete_response.status_code == 204
