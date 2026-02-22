"""Alert model for the monitoring module."""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
)
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import (
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from config.database import Base


class AlertType(str, Enum):
    """Types of alerts."""

    # System alerts
    SYSTEM_DOWN = "system_down"
    HIGH_CPU_USAGE = "high_cpu_usage"
    HIGH_MEMORY_USAGE = "high_memory_usage"
    DISK_SPACE_LOW = "disk_space_low"
    DATABASE_CONNECTION_FAILED = "database_connection_failed"

    # Security alerts
    MULTIPLE_LOGIN_FAILURES = "multiple_login_failures"
    SUSPICIOUS_ACTIVITY = "suspicious_activity"
    UNAUTHORIZED_ACCESS_ATTEMPT = "unauthorized_access_attempt"
    POTENTIAL_FRAUD = "potential_fraud"
    SECURITY_BREACH = "security_breach"

    # Business alerts
    HIGH_ERROR_RATE = "high_error_rate"
    SLOW_RESPONSE_TIME = "slow_response_time"
    SERVICE_UNAVAILABLE = "service_unavailable"
    PAYMENT_FAILURE_SPIKE = "payment_failure_spike"
    DOCUMENT_PROCESSING_DELAY = "document_processing_delay"

    # Anomaly alerts
    UNUSUAL_TRAFFIC_PATTERN = "unusual_traffic_pattern"
    UNEXPECTED_DATA_VOLUME = "unexpected_data_volume"
    ANOMALOUS_USER_BEHAVIOR = "anomalous_user_behavior"

    # Compliance alerts
    AUDIT_LOG_MISSING = "audit_log_missing"
    DATA_RETENTION_VIOLATION = "data_retention_violation"
    COMPLIANCE_THRESHOLD_EXCEEDED = "compliance_threshold_exceeded"


class AlertSeverity(str, Enum):
    """Alert severity levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AlertStatus(str, Enum):
    """Alert status."""

    ACTIVE = "active"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"
    SUPPRESSED = "suppressed"
    ESCALATED = "escalated"


class AlertCategory(str, Enum):
    """Alert categories."""

    INFRASTRUCTURE = "infrastructure"
    SECURITY = "security"
    APPLICATION = "application"
    BUSINESS = "business"
    COMPLIANCE = "compliance"


class Alert(Base):
    __table_args__ = {"extend_existing": True}
    """Alert model for system notifications and warnings."""

    __tablename__ = "monitoring_alerts"

    id = Column(Integer, primary_key=True, index=True)

    # Alert identification
    alert_type = Column(SQLEnum(AlertType), nullable=False, index=True)
    severity = Column(SQLEnum(AlertSeverity), nullable=False, index=True)
    category = Column(SQLEnum(AlertCategory), nullable=False, index=True)
    status = Column(SQLEnum(AlertStatus), default=AlertStatus.ACTIVE, index=True)

    # Alert content
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    recommendation = Column(Text)  # Suggested action

    # Source information
    source_module = Column(String(50), index=True)
    source_component = Column(String(100), index=True)
    source_metric_id = Column(
        Integer, ForeignKey("monitoring_system_metrics.id"), nullable=True
    )

    # Context information
    affected_resource_type = Column(String(100))
    affected_resource_id = Column(Integer)
    affected_users_count = Column(Integer)

    # Geographic context
    province = Column(String(100), index=True)
    municipality = Column(String(100), index=True)

    # Time information
    created_at = Column(DateTime, default=func.now(), nullable=False, index=True)
    first_occurrence = Column(DateTime, default=func.now(), nullable=False)
    last_occurrence = Column(DateTime, default=func.now(), nullable=False)
    occurrence_count = Column(Integer, default=1)

    # Resolution information
    acknowledged_at = Column(DateTime)
    acknowledged_by = Column(Integer, ForeignKey("monitoring_users.id"))
    resolved_at = Column(DateTime)
    resolved_by = Column(Integer, ForeignKey("monitoring_users.id"))
    resolution_notes = Column(Text)

    # Alert data
    trigger_conditions = Column(JSON)  # Conditions that triggered the alert
    alert_data = Column(JSON)  # Additional alert-specific data
    tags = Column(JSON)  # Tags for filtering and categorization

    # Notification settings
    notification_sent = Column(Boolean, default=False)
    notification_channels = Column(JSON)  # email, sms, webhook, etc.
    escalation_level = Column(Integer, default=0)

    # Suppression and grouping
    is_suppressed = Column(Boolean, default=False)
    suppressed_until = Column(DateTime)
    parent_alert_id = Column(Integer, ForeignKey("monitoring_alerts.id"))
    group_key = Column(String(100), index=True)  # For grouping similar alerts

    # Relationships
    source_metric = relationship("SystemMetric", foreign_keys=[source_metric_id])
    parent_alert = relationship("Alert", remote_side=[id])
    child_alerts = relationship("Alert", remote_side=[parent_alert_id])

    def __repr__(self):
        return f"<Alert(id={self.id}, type={self.alert_type}, severity={self.severity}, status={self.status})>"

    @property
    def is_active(self) -> bool:
        """Check if alert is currently active."""
        return self.status == AlertStatus.ACTIVE

    @property
    def is_critical(self) -> bool:
        """Check if alert is critical severity."""
        return self.severity == AlertSeverity.CRITICAL

    @property
    def duration_minutes(self) -> Optional[int]:
        """Calculate alert duration in minutes."""
        if self.resolved_at:
            return int((self.resolved_at - self.created_at).total_seconds() / 60)
        return int((datetime.utcnow() - self.created_at).total_seconds() / 60)

    @property
    def is_overdue(self) -> bool:
        """Check if alert has been active too long based on severity."""
        if self.status != AlertStatus.ACTIVE:
            return False

        duration = self.duration_minutes
        if duration is None:
            return False

        # Define SLA thresholds based on severity
        sla_thresholds = {
            AlertSeverity.CRITICAL: 15,  # 15 minutes
            AlertSeverity.HIGH: 60,  # 1 hour
            AlertSeverity.MEDIUM: 240,  # 4 hours
            AlertSeverity.LOW: 1440,  # 24 hours
        }

        threshold = sla_thresholds.get(self.severity, 1440)
        return duration > threshold

    def to_dict(self) -> Dict[str, Any]:
        """Convert alert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "alert_type": self.alert_type.value,
            "severity": self.severity.value,
            "category": self.category.value,
            "status": self.status.value,
            "title": self.title,
            "description": self.description,
            "recommendation": self.recommendation,
            "source_module": self.source_module,
            "source_component": self.source_component,
            "source_metric_id": self.source_metric_id,
            "affected_resource_type": self.affected_resource_type,
            "affected_resource_id": self.affected_resource_id,
            "affected_users_count": self.affected_users_count,
            "province": self.province,
            "municipality": self.municipality,
            "created_at": self.created_at.isoformat(),
            "first_occurrence": self.first_occurrence.isoformat(),
            "last_occurrence": self.last_occurrence.isoformat(),
            "occurrence_count": self.occurrence_count,
            "acknowledged_at": (
                self.acknowledged_at.isoformat() if self.acknowledged_at else None
            ),
            "acknowledged_by": self.acknowledged_by,
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
            "resolved_by": self.resolved_by,
            "resolution_notes": self.resolution_notes,
            "trigger_conditions": self.trigger_conditions,
            "alert_data": self.alert_data,
            "tags": self.tags,
            "notification_sent": self.notification_sent,
            "notification_channels": self.notification_channels,
            "escalation_level": self.escalation_level,
            "is_suppressed": self.is_suppressed,
            "suppressed_until": (
                self.suppressed_until.isoformat() if self.suppressed_until else None
            ),
            "parent_alert_id": self.parent_alert_id,
            "group_key": self.group_key,
            "is_active": self.is_active,
            "is_critical": self.is_critical,
            "duration_minutes": self.duration_minutes,
            "is_overdue": self.is_overdue,
        }

