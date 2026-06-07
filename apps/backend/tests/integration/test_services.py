import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import pytest

pytest.importorskip("backend.main")

from httpx import AsyncClient

from apps.backend.main import app


@pytest.mark.external
@pytest.mark.asyncio
class TestServices:
    @pytest.fixture(scope="module")
    async def async_client(self):
        async with AsyncClient(app=app, base_url="http://testserver") as client:
            yield client

    async def test_create_user_service(self, async_client):
        # Example test for user creation service
        # Replace with actual service call and assertions
        response = await async_client.post(
            "/users/", json={"username": "testuser", "password": "password123"}
        )
        assert response.status_code == 201
        assert response.json()["username"] == "testuser"

    async def test_send_notification_service(self, async_client):
        # Example test for notification service
        # Replace with actual service call and assertions
        response = await async_client.post(
            "/notifications/", json={"user_id": 1, "message": "Hello, World!"}
        )
        assert response.status_code == 200
        assert response.json()["status"] == "sent"
