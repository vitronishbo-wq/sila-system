"""
Pydantic schemas for the User entity.
Used for data validation and clear typing across the application.
"""
from typing import Optional, List
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    """Base schema for user data."""
    email: EmailStr
    is_active: bool = True
    role: str

class User(UserBase):
    """Schema representing a user object retrieved from the system."""
    id: Optional[str] = None
    province: Optional[str] = None
    municipality: Optional[str] = None
    allowed_modules: List[str] = []

    class Config:
        from_attributes = True

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None