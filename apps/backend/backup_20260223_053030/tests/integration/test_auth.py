# backend/tests/test_auth.py
"""
Comprehensive tests for authentication functionality.
"""

from datetime import datetime, timedelta
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.services.auth_service import AuthService
from core.db.models.user import RefreshToken, User


class TestAuthEndpoints:
    @pytest.fixture
    def client(self):
        return TestClient(app)

    @pytest.fixture
    def mock_user(self):
        return User(
            id="test-user-id",
            email="test@example.com",
            hashed_password=settings.PASSWORD,
            full_name="Test User",
            is_active=True,
        )

    @pytest.fixture
    def mock_db(self):
        return AsyncMock(spec=AsyncSession)

    def test_login_success(self, client, mock_user):
        with (patch("app.services.auth_service.AuthService.authenticate") as mock_auth,
            patch("app.services.auth_service.AuthService.create_access_token") as mock_access,
            patch("app.services.auth_service.AuthService.create_refresh_token") as mock_refresh,):
            mock_auth.return_value = mock_user
            mock_access.return_value = "access_token_123"
            mock_refresh.return_value = "refresh_token_123"

            response = client.post("/api/v1/auth/login/access-token",
                data={"username": "test@example.com", "password": "secret"},)
            assert response.status_code == 200
            data = response.json()
            assert "access_token" in data
            assert "refresh_token" in data
            assert data["token_type"] == "bearer"

    def test_login_invalid_credentials(self, client):
        with patch("app.services.auth_service.AuthService.authenticate") as mock_auth:
            mock_auth.return_value = None
            response = client.post("/api/v1/auth/login/access-token",
                data={"username": "test@example.com", "password": "wrong"},)
            assert response.status_code == 400

    def test_login_inactive_user(self, client, mock_user):
        mock_user.is_active = False
        with patch("app.services.auth_service.AuthService.authenticate") as mock_auth:
            mock_auth.return_value = mock_user
            response = client.post("/api/v1/auth/login/access-token",
                data={"username": "test@example.com", "password": "secret"},)
            assert response.status_code == 400

    def test_refresh_token_success(self, client):
        with patch("app.services.auth_service.AuthService.refresh_access_token") as mock_refresh:
            mock_refresh.return_value = {
                "access_token": "new_access_token",
                "token_type": "bearer",
                "refresh_token": "new_refresh_token",
            }
            response = client.post("/api/v1/auth/refresh", json={"refresh_token": "valid_token"})
            assert response.status_code == 200

    def test_logout_success(self, client):
        with patch("app.services.auth_service.AuthService.revoke_refresh_token") as mock_revoke:
            mock_revoke.return_value = True
            response = client.post("/api/v1/auth/logout", json={"refresh_token": "valid_token"})
            assert response.status_code == 200

    def test_register_success(self, client):
        with (patch("app.services.user_service.UserService.get_by_email") as mock_get,
            patch("app.services.user_service.UserService.create") as mock_create,):
            mock_get.return_value = None
            mock_create.return_value = User(id="new-user-id",
                email="newuser@example.com",
                full_name="New User",
                is_active=True,)
            response = client.post("/api/v1/auth/register",
                json={"email": "newuser@example.com", "name": "New User", "password": "123"},)
            assert response.status_code == 200


class TestAuthService:
    @pytest.fixture
    def mock_user(self):
        return User(id="test-user-id",
            email="test@example.com",
            hashed_settings.PASSWORD,
            is_active=True,)

    @pytest.fixture
    def mock_db(self):
        return AsyncMock(spec=AsyncSession)

    @pytest.mark.asyncio
    async def test_authenticate_success(self, mock_user, mock_db):
        with patch("app.db.models.user.User.get_by_email") as mock_get:
            mock_get.return_value = mock_user
            result = await AuthService.authenticate(mock_db, "test@example.com", "secret")
            assert result == mock_user

    @pytest.mark.asyncio
    async def test_create_refresh_token(self, mock_db):
        with patch("app.db.models.user.RefreshToken") as mock_token_class:
            mock_token = RefreshToken(id=1,
                token="test_token",
                user_id="test-user-id",
                expires_at=datetime.utcnow() + timedelta(days=7),)
            mock_token_class.return_value = mock_token
            result = await AuthService.create_refresh_token(mock_db, "test-user-id")
            assert result == "test_token"


class TestProtectedRoutes:
    @pytest.fixture
    def client(self):
        return TestClient(app)

    def test_protected_route_without_token(self, client):
        response = client.get("/api/v1/auth/login/test-token")
        assert response.status_code in [401, 422]
