"""
Alert Schemas for Monitoring Module
Pydantic models for API request/response validation
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


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


class AlertAcknowledge(BaseModel):
    """Schema for acknowledging an alert."""

    model_config = ConfigDict(from_attributes=True)

    user_id: str = Field(..., description="ID of the user acknowledging the alert")
    note: Optional[str] = Field(
        None, description="Optional note about the acknowledgment"
    )


class AlertSchema(BaseModel):
    """Base schema for Alert."""

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    id: int
    type: AlertType
    severity: AlertSeverity
    status: AlertStatus
    message: str
    title: Optional[str] = None
    description: Optional[str] = None
    created_at: Optional[datetime] = None
