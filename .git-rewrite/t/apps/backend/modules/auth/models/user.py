"""User domain models (ORM + DTOs) adapted for MariaDB."""

from datetime import datetime
from enum import Enum
from uuid import UUID
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, EmailStr, Field
from sqlalchemy import Boolean, Column, DateTime, String, UUID as SQLUUID, Enum as SAEnum
from sqlalchemy.orm import relationship

from core.db.base_class import Base


class AdministrativeLevel(str, Enum):
    LOCAL = "LOCAL"
    PROVINCIAL = "PROVINCIAL"
    CENTRAL = "CENTRAL"


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"
    GUEST = "GUEST"


class User(Base):
    """ORM model representing an application user (MariaDB compatible)."""

    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id = Column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    email = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, nullable=True, default=True)
    is_superuser = Column(Boolean, nullable=True, default=False)
    is_verified = Column(Boolean, nullable=True, default=False)
    created_at = Column(
        DateTime(timezone=True), nullable=True, default=datetime.utcnow
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=True,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
    level = Column(
        SAEnum(AdministrativeLevel, native_enum=False), nullable=True
    )
    region_id = Column(SQLUUID(as_uuid=True), nullable=True)
    
    # Relacionamentos
    activity_logs = relationship(
        "ActivityLog",
        back_populates="user",
        foreign_keys="ActivityLog.user_id",
        lazy="noload",
    )


# =========================
# Pydantic Schemas
# =========================

class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None
    is_active: bool = True
    is_superuser: bool = False
    level: AdministrativeLevel | None = None
    region_id: UUID | None = None


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class UserUpdate(BaseModel):
    full_name: str | None = None
    password: str | None = None
    is_active: bool | None = None
    is_superuser: bool | None = None
    level: AdministrativeLevel | None = None
    region_id: UUID | None = None


class UserRead(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    is_verified: bool

    model_config = ConfigDict(from_attributes=True)
