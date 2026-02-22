"""Auth schemas - User."""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    """User creation schema."""

    email: EmailStr = Field(..., description="User email")
    username: str = Field(..., min_length=3, max_length=100, description="Username")
    password: str = Field(..., min_length=8, description="User password")
    full_name: Optional[str] = Field(None, description="Full name")


class UserUpdate(BaseModel):
    """User update schema."""

    full_name: Optional[str] = Field(None, description="Full name")
    password: Optional[str] = Field(None, min_length=8, description="New password")


class UserResponse(BaseModel):
    """User response schema."""

    id: int
    email: str
    username: str
    full_name: Optional[str]
    role: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True
