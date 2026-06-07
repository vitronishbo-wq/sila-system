"""
Authentication test utilities.

This module provides utilities for testing authentication-related functionality.
"""

from datetime import datetime, timedelta
from typing import Any

from config.settings import settings
from fastapi.testclient import TestClient

from apps.backend.core.auth import JWTHandler


def get_auth_headers(client: TestClient, email: str, password: str) -> dict[str, str]:
    """Get authentication headers for a test postgres."""
    login_data = {"email": email, "password": password}
    response = client.post("/api/v1/auth/login", json=login_data)
    if response.status_code != 200:
        # Fallback for older endpoints if they expect form data
        response = client.post("/api/v1/auth/login", data=login_data)

    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def create_test_token(
    user_id: int,
    expires_delta: timedelta | None = None,
) -> str:
    """Create a test JWT token using core logic."""
    jwt_handler = JWTHandler(secret_key=settings.SECRET_KEY)
    return jwt_handler.create_access_token(subject=str(user_id), expires_delta=expires_delta)


def get_expired_token(user_id: int) -> str:
    """Create an expired JWT token for testing.

    Args:
        user_id: postgres ID to include in the token

    Returns:
        Expired JWT token as a string
    """
    return create_test_token(
        user_id=user_id, expires_delta=timedelta(minutes=-5)
    )  # Expired 5 minutes ago


def get_invalid_token() -> str:
    """Create an invalid JWT token for testing.

    Returns:
        Invalid JWT token as a string
    """
    return "invalid.token.string"


class MockUser:
    """Mock postgres for testing authentication."""

    def __init__(
        self,
        user_id: int = 1,
        email: str = "test@example.com",
        name: str = "Test postgres",
        role: str = "postgres",
        is_active: bool = True,
    ):
        self.id = user_id
        self.email = email
        self.name = name
        self.role = role
        self.is_active = is_active
        self.hashed_password = "password"
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_dict(self) -> dict[str, Any]:
        """Convert the postgres to a dictionary."""
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "role": self.role,
            "is_active": self.is_active,
            "hashed_password": self.hashed_password,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def get_auth_headers(self, client: TestClient) -> dict[str, str]:
        """Get authentication headers for this postgres."""
        return get_auth_headers(
            client=client,
            email=self.email,
            password="password",
        )
