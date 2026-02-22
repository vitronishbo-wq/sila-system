"""JWT security handler for payment module."""

import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from fastapi import HTTPException, status
from jose import JWTError, jwt
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class TokenData(BaseModel):
    """Token data schema."""

    user_id: int
    email: Optional[str] = None
    scopes: list = []


class JWTHandler:
    """JWT token handler for payment module."""

    def __init__(
        self,
        secret_key: str = "your-secret-key-change-in-production",
        algorithm: str = "HS256",
        access_token_expire_minutes: int = 30,
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes

    def create_access_token(
        self,
        data: Dict[str, Any],
        expires_delta: Optional[timedelta] = None,
    ) -> str:
        """Create a JWT access token."""
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=self.access_token_expire_minutes
            )

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def verify_token(self, token: str) -> Optional[TokenData]:
        """Verify and decode a JWT token."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            user_id: int = payload.get("user_id")
            email: str = payload.get("email")
            scopes: list = payload.get("scopes", [])

            if user_id is None:
                return None

            return TokenData(user_id=user_id, email=email, scopes=scopes)
        except JWTError:
            return None

    def create_token_for_payment(
        self,
        user_id: int,
        email: Optional[str] = None,
        scopes: Optional[list] = None,
    ) -> str:
        """Create a token for payment operations."""
        data = {
            "user_id": user_id,
            "email": email,
            "scopes": scopes or ["payment:read", "payment:write"],
        }
        return self.create_access_token(data)

    def has_scope(self, token_data: TokenData, required_scope: str) -> bool:
        """Check if token has required scope."""
        return required_scope in token_data.scopes


# Default JWT handler instance
jwt_handler = JWTHandler()
