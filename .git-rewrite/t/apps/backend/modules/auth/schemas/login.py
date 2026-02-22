"""Auth schemas - Login & Token."""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class LoginRequest(BaseModel):
    """Login request schema."""

    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., min_length=8, description="User password")


class TokenResponse(BaseModel):
    """Token response schema."""

    access_token: str = Field(..., description="JWT access token")
    refresh_token: Optional[str] = Field(None, description="JWT refresh token")
    token_type: str = Field(default="Bearer", description="Token type")


class UserLoginResponse(BaseModel):
    """User login response with token."""

    id: int
    email: str
    username: str
    full_name: Optional[str]
    role: str
    access_token: str
    token_type: str = "Bearer"
