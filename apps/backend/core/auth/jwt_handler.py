"""
Centralized JWT Token Handler for SILA

Consolidates all JWT token creation, validation, and management.
Replaces scattered JWT implementations across the system.

Features:
- Access token creation and validation
- Refresh token management
- Token expiration handling
- UUID serialization support
- Direct secret key configuration

Used by: All 60+ SILA modules for authentication
"""

from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import UUID

import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from pydantic import BaseModel, Field


class TokenConfig:
    """Centralized token configuration"""

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 129600  # 90 days
    REFRESH_TOKEN_EXPIRE_DAYS: int = 90
    ALGORITHM: str = "HS256"

    @classmethod
    def set_secret(cls, secret: str) -> None:
        """Set the secret key for token signing"""
        cls.SECRET_KEY = secret


class DecodedToken(BaseModel):
    """Schema for JWT payload validation and access"""

    sub: str = Field(..., description="Subject (user ID)")
    exp: int = Field(..., description="Expiration timestamp")
    iat: int = Field(..., description="Issued at timestamp")
    type: str = Field(..., description="Token type: 'access' or 'refresh'")

    def get(self, key: str, default: Any = None) -> Any:
        """Get token claim by key with default fallback"""
        return getattr(self, key, default)

    def __getitem__(self, key: str) -> Any:
        """Dict-like access to token claims"""
        return getattr(self, key)


class JWTHandler:
    """
    Centralized JWT handler for all SILA token operations.

    Handles:
    - Token creation (access & refresh)
    - Token validation
    - Token decoding with claim extraction
    - Expiration verification
    - UUID serialization in claims
    """

    def __init__(self, secret_key: str | None = None):
        """
        Initialize JWT handler.

        Args:
            secret_key: JWT signing secret. Uses TokenConfig.SECRET_KEY if not provided.
        """
        self.secret_key = secret_key or getattr(TokenConfig, "SECRET_KEY", None)
        if not self.secret_key:
            raise ValueError(
                "JWT secret key not configured. "
                "Set via TokenConfig.set_secret() or pass to __init__"
            )
        self.algorithm = TokenConfig.ALGORITHM

    def _serialize_payload(self, payload: dict[str, Any]) -> dict[str, Any]:
        """
        Serialize payload for JWT encoding.
        Converts UUID objects to strings for JSON compatibility.

        Args:
            payload: Dictionary with potential UUID values

        Returns:
            Serialized payload with all values JSON-compatible
        """
        return {k: str(v) if isinstance(v, UUID) else v for k, v in payload.items()}

    def create_access_token(
        self,
        subject: str,
        data: dict[str, Any] | None = None,
        expires_delta: timedelta | None = None,
    ) -> str:
        """
        Create a signed access token.

        Args:
            subject: Subject claim (typically user ID)
            data: Additional claims to include in token
            expires_delta: Custom expiration time (default: 90 days)

        Returns:
            Signed JWT access token
        """
        claims = data.copy() if data else {}
        claims.update({"type": "access", "sub": str(subject)})

        expiry = expires_delta or timedelta(minutes=TokenConfig.ACCESS_TOKEN_EXPIRE_MINUTES)
        return self._encode_token(claims, expiry)

    def create_refresh_token(
        self,
        subject: str,
        data: dict[str, Any] | None = None,
        expires_delta: timedelta | None = None,
    ) -> str:
        """
        Create a signed refresh token.

        Args:
            subject: Subject claim (typically user ID)
            data: Additional claims to include in token
            expires_delta: Custom expiration time (default: 90 days)

        Returns:
            Signed JWT refresh token
        """
        claims = data.copy() if data else {}
        claims.update({"type": "refresh", "sub": str(subject)})

        expiry = expires_delta or timedelta(days=TokenConfig.REFRESH_TOKEN_EXPIRE_DAYS)
        return self._encode_token(claims, expiry)

    def _encode_token(self, payload: dict[str, Any], expires_delta: timedelta) -> str:
        """
        Internal method to encode and sign a token.

        Args:
            payload: Claims to encode
            expires_delta: Token expiration duration

        Returns:
            Signed JWT token
        """
        to_encode = self._serialize_payload(payload)
        now = datetime.now(UTC)
        expire = now + expires_delta

        to_encode.update({"exp": int(expire.timestamp()), "iat": int(now.timestamp())})

        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def decode_token(
        self,
        token: str,
        verify_exp: bool = True,
    ) -> dict[str, Any]:
        """
        Decode and validate a token without type checking.

        Args:
            token: JWT token string
            verify_exp: Whether to verify expiration

        Returns:
            Decoded token payload as dictionary

        Raises:
            InvalidTokenError: If token is invalid or signature verification fails
            ExpiredSignatureError: If token has expired and verify_exp=True
        """
        try:
            options = {"verify_exp": verify_exp}
            payload = jwt.decode(
                token, self.secret_key, algorithms=[self.algorithm], options=options
            )
            return payload
        except ExpiredSignatureError as err:
            raise ExpiredSignatureError("Token has expired") from err
        except Exception as e:
            raise InvalidTokenError(f"Token validation failed: {str(e)}") from e

    def decode_access_token(
        self,
        token: str,
        verify_exp: bool = True,
    ) -> DecodedToken:
        """
        Decode and validate an access token.

        Args:
            token: JWT access token string
            verify_exp: Whether to verify expiration

        Returns:
            Decoded token with type validation

        Raises:
            InvalidTokenError: If token is not an access token or invalid
        """
        payload = self.decode_token(token, verify_exp=verify_exp)

        if payload.get("type") != "access":
            raise InvalidTokenError("Invalid token: Expected access token")

        return DecodedToken(**payload)

    def decode_refresh_token(
        self,
        token: str,
        verify_exp: bool = True,
    ) -> DecodedToken:
        """
        Decode and validate a refresh token.

        Args:
            token: JWT refresh token string
            verify_exp: Whether to verify expiration

        Returns:
            Decoded token with type validation

        Raises:
            InvalidTokenError: If token is not a refresh token or invalid
        """
        payload = self.decode_token(token, verify_exp=verify_exp)

        if payload.get("type") != "refresh":
            raise InvalidTokenError("Invalid token: Expected refresh token")

        return DecodedToken(**payload)

    def get_user_id_from_token(self, token: str) -> str | None:
        """
        Extract user ID from token without full validation.
        Useful for identifying users in error responses.

        Args:
            token: JWT token string

        Returns:
            User ID (subject) or None if token invalid
        """
        try:
            payload = self.decode_token(token, verify_exp=False)
            return payload.get("sub")
        except Exception:
            return None
