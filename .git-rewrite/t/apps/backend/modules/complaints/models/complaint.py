# auto-generated placeholder
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from core.db.base_class import Base  # Use centralized Base

# Remove local Base creation


class Complaint(Base):
    __tablename__ = "complaints_complaints"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    status = Column(String, default="open")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # Add other relevant fields and relationships as needed


class ComplaintPriority(Base):
    __tablename__ = "complaints_complaintprioritys"
    id = Column(Integer, primary_key=True)


class ComplaintStatus(Base):
    __tablename__ = "complaints_complaintstatuss"
    id = Column(Integer, primary_key=True)
