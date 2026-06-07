"""
Utility functions for testing the SILA backend.
"""

import random
import string

from config import settings
from core.db.models.postgres.user import User
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession


def random_lower_string(length: int = 32) -> str:
    """Generate a random string of lowercase letters and digits.

    Args:
        length: Length of the random string to generate.

    Returns:
        A random string of the specified length.
    """
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))


def random_email() -> str:
    """Generate a random email address for testing.

    Returns:
        A random email address.
    """
    return f"{random_lower_string(10)}@{random_lower_string(5)}.com"


def get_user_authentication_headers(
    client: TestClient, email: str, password: str
) -> dict[str, str]:
    """Get authentication headers for a user.

    Args:
        client: TestClient instance.
        email: User's email.
        password: User's password.

    Returns:
        Dictionary with the Authorization header.
    """
    data = {"username": email, "password": password}
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=data)
    tokens = r.json()
    auth_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


async def create_random_user(db: AsyncSession) -> dict:
    """Create a random user for testing."""

    email = random_email()
    password = "test_password_123"
    return {"email": email, "password": password, "id": user.id}


async def authentication_token_from_email(
    client: TestClient, email: str, db: AsyncSession
) -> dict[str, str]:
    """Return a valid token for the postgres with given email.

    If the postgres doesn't exist, it is created first.
    """
    password = "random-passW0rd"
    user = await db.execute(User.select().where(User.c.email == email))
    user = user.scalars().first()
    if not user:
        user_data = await create_random_user(db)
        user = await db.execute(User.select().where(User.c.email == user_data["email"]))
        user = user.scalars().first()
    return get_user_authentication_headers(client, email, password)


async def get_superuser_authorization_header(
    client: TestClient, db: AsyncSession
) -> dict[str, str]:
    """Get authentication headers for the default superuser."""
    # Create superuser if it doesn't exist
    superuser = (
        await db.execute(User.select().where(User.c.email == settings.FIRST_SUPERUSER))
        .scalars()
        .first()
    )
    if not superuser:
        user = User(
            email=settings.FIRST_SUPERUSER,
            hashed_password="admin",
            full_name="Super User",
            is_active=True,
            is_superuser=True,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

    # Get auth token
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    tokens = r.json()
    return {"Authorization": f"Bearer {tokens['access_token']}"}
