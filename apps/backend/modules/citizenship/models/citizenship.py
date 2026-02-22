"""CitizenshipRequest ORM Model."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from config.database import Base


class CitizenshipRequest(Base):
    """CitizenshipRequest model for citizenship operations."""
    
    __tablename__ = "citizenship_requests"
    __table_args__ = {"extend_existing": True}
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    bi_number = Column(String(50), nullable=False)
    status = Column(String(50), default="pending", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

