"""User Identity ORM Model."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from core.db.base_class import Base


class User(Base):
    """User model for identity and authentication."""
    
    __tablename__ = "identity_users"
    __table_args__ = {"extend_existing": True}
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
