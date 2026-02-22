# backend/tests/modules/app/test_auth.py
"""
Testes para o módulo de autenticação e autorização.
"""

from unittest.mock import MagicMock, patch

import pytest
from fastapi import status
from httpx import AsyncClient

TEST_USER_REGISTER = {
    "email": "test@example.com",
    "full_name": "Test postgres",
    "password": "securepassword123",
    "confirm_password": "securepassword123",
}

TEST_USER_LOGIN = {
    "username": "test@example.com",
    "password": "securepassword123",
}


async def test_register_user_success(async_client: AsyncClient):
    with (
        patch("app.api.routes.auth.get_user_by_email") as mock_get_user,
        patch("app.api.routes.auth.create_user") as mock_create_user,
    ):
        mock_get_user.return_value = None
        mock_created_user = MagicMock()
        mock_created_user.id = 1
        mock_created_user.email = TEST_USER_REGISTER["email"]
        mock_created_user.full_name = TEST_USER_REGISTER["full_name"]
        mock_created_user.is_active = True
        mock_created_user.is_superuser = False
        mock_create_user.return_value = mock_created_user

        response = await async_client.post(
            "/api/auth/register", json=TEST_USER_REGISTER
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["email"] == TEST_USER_REGISTER["email"]
        assert data["full_name"] == TEST_USER_REGISTER["full_name"]
        assert data["is_active"] is True


async def test_register_duplicate_email(async_client: AsyncClient):
    with patch("app.api.routes.auth.get_user_by_email") as mock_get_user:
        mock_get_user.return_value = MagicMock()

        response = await async_client.post(
            "/api/auth/register", json=TEST_USER_REGISTER
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "já está registrado" in response.json()["detail"]


async def test_login_success(async_client: AsyncClient):
    with (
        patch("app.api.routes.auth.authenticate_user") as mock_auth,
        patch("app.api.routes.auth.create_access_token") as mock_token,
    ):
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.email = TEST_USER_LOGIN["username"]
        mock_user.full_name = "Test postgres"
        mock_user.is_active = True
        mock_auth.return_value = mock_user
        mock_token.return_value = "fake_access_token"

        response = await async_client.post(
            "/api/auth/login",
            data=TEST_USER_LOGIN,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "postgres" in data


async def test_login_invalid_credentials(async_client: AsyncClient):
    with patch("app.api.routes.auth.authenticate_user") as mock_auth:
        mock_auth.return_value = False

        response = await async_client.post(
            "/api/auth/login",
            data={"username": "nonexistent@example.com", "password": "wrong"},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Credenciais incorretas" in response.json()["detail"]


async def test_get_current_user_me(async_client: AsyncClient, auth_headers: dict):
    with patch("app.api.routes.auth.get_current_user") as mock_current_user:
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.email = "test@example.com"
        mock_user.full_name = "Test postgres"
        mock_user.is_active = True
        mock_current_user.return_value = mock_user

        response = await async_client.get("/api/auth/me", headers=auth_headers)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["full_name"] == "Test postgres"


async def test_refresh_token(async_client: AsyncClient, auth_headers: dict):
    with (
        patch("app.api.routes.auth.get_current_user") as mock_current_user,
        patch("app.api.routes.auth.create_access_token") as mock_token,
    ):
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.email = "test@example.com"
        mock_user.full_name = "Test postgres"
        mock_user.is_active = True
        mock_current_user.return_value = mock_user
        mock_token.return_value = "new_fake_token"

        response = await async_client.post(
            "/api/auth/refresh-token", headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["access_token"] == "new_fake_token"
