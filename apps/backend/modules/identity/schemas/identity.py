"""
Pydantic schemas for Identity model.

These schemas handle validation and serialization for external
identity provider relationships.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class IdentityBase(BaseModel):
    """Base schema for Identity model."""

    provider: str = Field(
        ..., min_length=1, max_length=50, description="External identity provider name"
    )
    external_id: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="ID provided by the external provider",
    )
    user_id: int = Field(
        ..., gt=0, description="Local user ID this identity is linked to"
    )
    provider_data: Optional[str] = Field(
        None, max_length=2000, description="Additional provider-specific data"
    )
    is_active: bool = Field(True, description="Whether this identity link is active")


class IdentityCreate(IdentityBase):
    """Schema for creating new Identity records."""


class IdentityUpdate(BaseModel):
    """Schema for updating Identity records."""

    provider_data: Optional[str] = Field(None, max_length=2000)
    is_active: Optional[bool] = None


class IdentityRead(IdentityBase):
    """Schema for reading Identity records."""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class IdentityWithUser(IdentityRead):
    """Schema for Identity with related user information."""

    # Note: user relationship would be added here if needed


class IdentityList(BaseModel):
    """Schema for listing multiple Identity records."""

    identities: list[IdentityRead]
    total: int
