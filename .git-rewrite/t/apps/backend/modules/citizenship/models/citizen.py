"""Citizen model for the citizenship module."""

from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.sql import func

from core.db.base_class import Base


class Citizen(Base):
    """Citizen model."""

    __tablename__ = "citizenship_citizens"

    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    address = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
