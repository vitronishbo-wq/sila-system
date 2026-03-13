"""
Schemas básicas para o sistema de autenticação
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from apps.backend.app.modules.identity.models.user import AdministrativeLevel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class RefreshTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: Optional[int] = None


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: Optional[str] = None
    is_active: bool = True
    is_superuser: bool = False
    level: AdministrativeLevel | None = None
    region_id: UUID | None = None


class UserRead(BaseModel):
    id: UUID
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool
    is_superuser: bool
    is_verified: bool
    level: AdministrativeLevel | None = None
    region_id: UUID | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
