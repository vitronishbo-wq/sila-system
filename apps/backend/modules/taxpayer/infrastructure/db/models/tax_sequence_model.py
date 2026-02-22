"""Tax Sequence SQLAlchemy Model"""

from sqlalchemy import Column, String, Integer, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

try:
    from ....core.database import Base
except ImportError:
    from sqlalchemy.orm import declarative_base
    Base = declarative_base()


class TaxSequenceModel(Base):
    """SQLAlchemy model for sequence control"""
    __tablename__ = "tax_sequences"
    __table_args__ = (
        Index("ix_sequences_type_year", "sequence_type", "year", unique=True),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    sequence_type = Column(String(50), nullable=False, index=True)  # declaration, debt, payment, certificate
    year = Column(Integer, nullable=False)
    last_value = Column(Integer, nullable=False, default=0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "sequence_type": self.sequence_type,
            "year": self.year,
            "last_value": self.last_value
        }
