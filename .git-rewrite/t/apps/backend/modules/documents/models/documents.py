"""Document ORM Model."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, ForeignKey
from core.db.base_class import Base


class Document(Base):
    """Document model for file uploads and management."""
    
    __tablename__ = "documents_documents"
    __table_args__ = {"extend_existing": True}
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    original_name = Column(String(255), nullable=False)
    file_size = Column(BigInteger, nullable=False)
    uploaded_by_id = Column(Integer, ForeignKey("identity_users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
