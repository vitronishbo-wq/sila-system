# /opt/sila-system/backend/modules/monitoring/models/audit_log.py

"""
Audit Log Models for Monitoring
Tracks all system actions for compliance and security auditing
"""

import enum
from datetime import datetime

from sqlalchemy import Column, DateTime
from sqlalchemy import Enum as SAEnum
from sqlalchemy import Index, Integer, String, Text

# Esta importação agora funcionará após a criação de base_class.py
from config.database import Base


class AuditLevel(str, enum.Enum):
    """Audit log severity levels."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class AuditAction(str, enum.Enum):
    """Audit log action types."""

    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    ACCESS = "access"
    LOGIN = "login"
    LOGOUT = "logout"
    EXPORT = "export"
    IMPORT = "import"


class AuditLog(Base):
    """
    Audit log model for tracking system actions.

    Stores comprehensive audit trail for compliance, security monitoring,
    and debugging purposes.
    """

    __tablename__ = "monitoring_audit_logs"
    __table_args__ = (
        # Indexes for fast lookup
        Index("ix_audit_logs_timestamp", "timestamp"),
        Index("ix_audit_logs_user_id", "user_id"),
        Index("ix_audit_logs_action", "action"),
        Index("ix_audit_logs_entity", "entity"),
        # Required option to allow table re-definition/extension across modules
        {"extend_existing": True},
    )

    id = Column(Integer, primary_key=True, index=True)

    # Action details
    action = Column(SAEnum(AuditAction), nullable=False, index=True)
    level = Column(SAEnum(AuditLevel), default=AuditLevel.INFO, nullable=False)

    # Entity information (what was affected)
    entity = Column(String(100), nullable=False, index=True)
    entity_id = Column(String(50), nullable=True, index=True)

    # User information (who performed the action)
    user_id = Column(String(50), nullable=True, index=True)
    user_email = Column(String(255), nullable=True)

    # Details
    message = Column(Text, nullable=True)
    details = Column(Text, nullable=True)  # Additional context (JSON string)

    # Metadata
    ip_address = Column(String(45), nullable=True)  # IPv4 or IPv6
    user_agent = Column(String(500), nullable=True)

    # Timestamp
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    def __repr__(self):
        return (
            f"<AuditLog(id={self.id}, action={self.action.value}, "
            f"level={self.level.value}, entity={self.entity}, "
            f"user_id={self.user_id})>"
        )

    def to_dict(self):
        """Convert audit log to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "action": self.action.value,
            "level": self.level.value,
            "entity": self.entity,
            "entity_id": self.entity_id,
            "user_id": self.user_id,
            "user_email": self.user_email,
            "message": self.message,
            "details": self.details,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
        }

