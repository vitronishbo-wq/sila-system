"""Core Security"""

import logging
import os
from datetime import datetime, timedelta
from typing import Any
from uuid import UUID

from apps.backend.app.core.settings import settings as app_settings

try:
    from jose import jwt
except ImportError:
    jwt = None
logger = logging.getLogger(__name__)

SECRET_KEY = getattr(app_settings, "SECRET_KEY", os.getenv("SECRET_KEY", "dev-secret-key"))
ALGORITHM = getattr(app_settings, "ALGORITHM", os.getenv("ALGORITHM", "HS256"))
ACCESS_TOKEN_EXPIRE_MINUTES = getattr(app_settings, "ACCESS_TOKEN_EXPIRE_MINUTES", 30)


class _FallbackIAMUser:
    def __init__(self):
        self.id = "test-user"
        self.username = "tester"
        self.email = "test@example.com"
        self.permissions = []
        self.roles = ["tester"]


class _FallbackIAMGateway:
    async def get_user(self, token: str):
        if not token:
            return None
        return _FallbackIAMUser()


def get_iam_client():
    """Compatibility IAM client provider used by legacy tests."""
    return _FallbackIAMGateway()


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create JWT access token."""
    if not jwt:
        raise RuntimeError("PyJWT not installed")
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    to_encode = {k: str(v) if isinstance(v, UUID) else v for k, v in to_encode.items()}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


class IAMClient:
    """IAM Client wrapper"""

    async def get_current_user(self, token: str) -> dict[str, Any] | None:
        """Get user"""
        client = get_iam_client()
        user = await client.get_user(token)
        if user:
            return {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "permissions": user.permissions,
                "roles": user.roles,
            }
        return None


def get_password_hash(pwd: str) -> str:
    from passlib.context import CryptContext

    return CryptContext(schemes=["bcrypt"], deprecated="auto").hash(pwd)


def verify_password(plain: str, hashed: str) -> bool:
    from passlib.context import CryptContext

    return CryptContext(schemes=["bcrypt"], deprecated="auto").verify(plain, hashed)


__all__ = [
    "ALGORITHM",
    "SECRET_KEY",
    "ACCESS_TOKEN_EXPIRE_MINUTES",
    "create_access_token",
    "IAMClient",
    "get_iam_client",
    "get_password_hash",
    "verify_password",
]
