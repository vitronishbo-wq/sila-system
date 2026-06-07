"""
Integration tests for user management endpoints.

This module contains tests for user-related operations such as
retrieving, updating, and managing user accounts.
"""

import pytest
from fastapi import status


class TestUsers:
    """Test cases for user management endpoints."""

    @pytest.mark.asyncio
    async def test_get_current_user(self, async_http_client, auth_headers, auth_user):
        """Test retrieving the currently authenticated user."""
        # Act
        response = await async_http_client.get("/api/v1/identity/users/me", headers=auth_headers)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["email"] == auth_user.email
        assert "hashed_password" not in data  # Sensitive data should be excluded
        assert "id" in data
        assert "created_at" in data

    @pytest.mark.asyncio
    async def test_update_current_user(self, async_http_client, auth_headers, auth_user):
        """Test updating the currently authenticated user."""
        # Arrange
        update_data = {"full_name": "Updated Name", "phone_number": "+5511999999999"}

        # Act
        response = await async_http_client.patch(
            "/api/v1/identity/users/me", headers=auth_headers, json=update_data
        )

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["full_name"] == update_data["full_name"]
        assert data["phone_number"] == update_data["phone_number"]

    @pytest.mark.asyncio
    async def test_update_password(self, async_http_client, auth_headers, auth_user):
        """Test updating the current user's password."""
        # Arrange
        password_data = {
            "current_password": "testpassword123",
            "new_password": "new_secure_password123",
            "new_password_confirm": "new_secure_password123",
        }

        # Act
        response = await async_http_client.put(
            "/api/v1/identity/users/me/password", headers=auth_headers, json=password_data
        )

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert "Password updated successfully" in response.json()["message"]

        # Verify new password works
        login_response = await async_http_client.post(
            "/api/v1/auth/login",
            data={
                "username": auth_user.email,
                "password": password_data["new_password"],
            },
        )
        assert login_response.status_code == status.HTTP_200_OK

    @pytest.mark.asyncio
    async def test_update_password_mismatch(self, async_http_client, auth_headers):
        """Test updating password with mismatched confirmation fails."""
        # Arrange
        password_data = {
            "current_password": "testpassword123",
            "new_password": "new_secure_password123",
            "new_password_confirm": "mismatched_password",
        }

        # Act
        response = await async_http_client.put(
            "/api/v1/identity/users/me/password", headers=auth_headers, json=password_data
        )

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "passwords do not match" in response.text.lower()

    @pytest.mark.asyncio
    async def test_list_users_as_admin(self, async_http_client, admin_headers, user_factory):
        """Test listing all users (admin only)."""
        # Arrange - create some test users
        user_factory.create_batch(3)

        # Act
        response = await async_http_client.get("/api/v1/identity/users/", headers=admin_headers)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 3  # Should include the admin and test users

    @pytest.mark.asyncio
    async def test_list_users_unauthorized(self, async_http_client, auth_headers):
        """Test that regular users cannot list all users."""
        # Act
        response = await async_http_client.get("/api/v1/identity/users/", headers=auth_headers)

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_get_user_by_id_as_admin(self, async_http_client, admin_headers, auth_user):
        """Test retrieving a user by ID (admin only)."""
        # Act - get the current user's ID
        me_response = await async_http_client.get(
            "/api/v1/identity/users/me", headers=admin_headers
        )
        user_id = me_response.json()["id"]

        # Get user by ID
        response = await async_http_client.get(
            f"/api/v1/identity/users/{user_id}", headers=admin_headers
        )

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == user_id
        assert data["email"] == auth_user.email

    @pytest.mark.asyncio
    async def test_update_user_as_admin(self, async_http_client, admin_headers, auth_user):
        """Test updating a user as an admin."""
        # Arrange - get the user ID
        me_response = await async_http_client.get(
            "/api/v1/identity/users/me", headers=admin_headers
        )
        user_id = me_response.json()["id"]

        update_data = {
            "is_active": False,
            "is_verified": True,
            "roles": ["user", "editor"],
        }

        # Act
        response = await async_http_client.patch(
            f"/api/v1/identity/users/{user_id}", headers=admin_headers, json=update_data
        )

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["is_active"] is False
        assert data["is_verified"] is True
        assert set(data["roles"]) == set(["user", "editor"])

    @pytest.mark.asyncio
    async def test_delete_user_as_admin(self, async_http_client, admin_headers, user_factory):
        """Test deleting a user as an admin."""
        # Arrange - create a test user
        test_user = user_factory.create()

        # Act
        response = await async_http_client.delete(
            f"/api/v1/identity/users/{test_user.id}", headers=admin_headers
        )

        # Assert
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify user no longer exists
        get_response = await async_http_client.get(
            f"/api/v1/identity/users/{test_user.id}", headers=admin_headers
        )
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
