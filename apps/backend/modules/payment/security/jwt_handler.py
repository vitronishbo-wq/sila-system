"""JWT security handler for payment module."""

import logging
from datetime import timedelta
from typing import Optional, Dict, Any

from fastapi import HTTPException, status
from core.auth import create_access_token, decode_token
from config.settings import settings
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
        secret_key: Optional[str] = None,
        algorithm: str = "HS256",
        access_token_expire_minutes: int = 129600,  # 90 dias em minutos
    ):
        self.secret_key = secret_key or settings.AUTH_SECRET_KEY
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes

    def create_access_token(
        self,
        data: Dict[str, Any],
        expires_delta: Optional[timedelta] = None,
    ) -> str:
        """Create a JWT access token."""
        expiry = expires_delta or timedelta(minutes=self.access_token_expire_minutes)
        return create_access_token(data=data, expires_delta=expiry)

    def verify_token(self, token: str) -> Optional[TokenData]:
        """Verify and decode a JWT token."""
        payload = decode_token(token)
        if not payload:
            return None
            
        user_id = payload.get("user_id") or payload.get("sub")
        email = payload.get("email")
        scopes = payload.get("scopes", [])

        if user_id is None:
            return None

        try:
            user_id = int(user_id)
        except (ValueError, TypeError):
            pass

        return TokenData(user_id=user_id, email=email, scopes=scopes)

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
