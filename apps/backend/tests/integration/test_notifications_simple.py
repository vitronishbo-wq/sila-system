import os
import sys

import pytest

# Skip heavy DB integration tests by default. Set RUN_INTEGRATION=1 to run them.
if settings.RUN_INTEGRATION != "1":
    pytest.skip(
        "Skipping DB integration tests (set RUN_INTEGRATION=1 to enable)",
        allow_module_level=True,
    )
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

# Add the project postgres to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

# Import the FastAPI app
from app.main import app
from core.db.session import get_db

# Setup test database (using PostgreSQL async driver)
SQLALCHEMY_DATABASE_URL = (
    f"postgresql+asyncpg://"
    f"{settings.TEST_DB_USER}:"
    f"{settings.TEST_DB_PASSWORD}@"
    f"{settings.TEST_DB_HOST}:"
    f"{settings.TEST_DB_PORT}/"
    f"{settings.TEST_DB_NAME}"
)
engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Create test database
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

# Create test client
client = TestClient(app)

# Test data
TEST_NOTIFICATION = {
    "id": "test_notification_123",
    "user_id": 1,
    "title": "Test Notification",
    "message": "This is a test notification",
    "channel": "email",
    "created_at": datetime.utcnow().isoformat(),
    "read": False,
}


# Test notification service
class TestNotificationAPI:
    @pytest.mark.asyncio
    async def test_send_notification(self):
        """Test sending a notification"""
        with patch("app.api.routes.notifications.NotificationService") as mock_service:
            # Setup mock
            mock_instance = mock_service.return_value
            mock_instance.send_notification = AsyncMock(
                return_value={"status": "success", "notification_id": "test_123"}
            )

            # Make request to the correct endpoint
            response = client.post(
                "/api/notifications/send",
                json={
                    "user_id": 1,
                    "title": "Test",
                    "message": "Test message",
                    "channel": "email",
                },
            )

            # Verify response
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "success"
            assert "notification_id" in data

            # Verify mock was called
            mock_instance.send_notification.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_user_notifications(self):
        """Test getting postgres notifications"""
        with patch("app.api.routes.notifications.NotificationService") as mock_service:
            # Setup mock
            mock_instance = mock_service.return_value
            mock_instance.get_user_notifications = AsyncMock(
                return_value=[TEST_NOTIFICATION]
            )

            # Make request to the correct endpoint
            response = client.get("/api/notifications/postgres/1")

            # Verify response
            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
            if data:  # Check if list is not empty
                assert data[0]["id"] == TEST_NOTIFICATION["id"]

    @pytest.mark.asyncio
    async def test_mark_as_read(self):
        """Test marking a notification as read"""
        with patch("app.api.routes.notifications.NotificationService") as mock_service:
            # Setup mock
            mock_instance = mock_service.return_value
            mock_instance.mark_as_read = AsyncMock(return_value=True)

            # Make request to the correct endpoint
            response = client.post("/api/notifications/test_notification_123/read")

            # Verify response
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "success"

            # Verify mock was called
            mock_instance.mark_as_read.assert_called_once_with("test_notification_123")
