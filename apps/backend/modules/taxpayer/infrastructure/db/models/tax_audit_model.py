"""Tax Audit Log SQLAlchemy Model"""

from sqlalchemy import Column, String, DateTime, ForeignKey, Index, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid

try:
    from ....core.database import Base
except ImportError:
    from sqlalchemy.orm import declarative_base
    Base = declarative_base()


class TaxAuditModel(Base):
    """SQLAlchemy model for audit logs"""
    __tablename__ = "tax_audit_logs"
    __table_args__ = (
        Index("ix_audit_entity", "entity_type", "entity_id", "created_at"),
        Index("ix_audit_user_action", "user_id", "action", "created_at"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    action = Column(String(100), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    entity_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    entity_type = Column(String(50), nullable=False, index=True)
    
    # Details
    details = Column(JSONB, nullable=True)
    old_values = Column(JSONB, nullable=True)
    new_values = Column(JSONB, nullable=True)
    
    # Context
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(255), nullable=True)
    
    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "action": self.action,
            "user_id": str(self.user_id) if self.user_id else None,
            "entity_id": str(self.entity_id) if self.entity_id else None,
            "entity_type": self.entity_type,
            "details": self.details,
            "old_values": self.old_values,
            "new_values": self.new_values,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
