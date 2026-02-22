# /opt/sila-system/backend/app/schemas/user.py

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
    role: str  # Used heavily by access_control.py (e.g., "admin", "auditor")


class User(UserBase):
    """Schema representing a user object retrieved from the system."""

    id: Optional[str] = None  # Used by access_control.can_view_audit_log

    # Geographic scope properties used by access_control.get_geographic_restrictions
    province: Optional[str] = None
    municipality: Optional[str] = None

    # Module restriction properties used by access_control._check_context_restrictions
    allowed_modules: List[str] = []

    class Config:
        # Permite que o modelo User seja criado a partir de um objeto ORM (ORM Mode foi renomeado para from_attributes em Pydantic v2)
        from_attributes = True


# Outros esquemas (criação, atualização, etc.)
class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None
