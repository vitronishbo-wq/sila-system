"""System metric model for the monitoring module."""

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
    Float,
    Integer,
    String,
)
from sqlalchemy.sql import func

from config.database import Base


class MetricType(str, Enum):
    """Types of system metrics."""

    # Performance metrics
    RESPONSE_TIME = "response_time"
    THROUGHPUT = "throughput"
    ERROR_RATE = "error_rate"
    CPU_USAGE = "cpu_usage"
    MEMORY_USAGE = "memory_usage"
    DISK_USAGE = "disk_usage"

    # Usage metrics
    ACTIVE_USERS = "active_users"
    CONCURRENT_SESSIONS = "concurrent_sessions"
    API_CALLS = "api_calls"
    PAGE_VIEWS = "page_views"

    # Business metrics
    CITIZEN_REGISTRATIONS = "citizen_registrations"
    DOCUMENT_REQUESTS = "document_requests"
    PAYMENT_TRANSACTIONS = "payment_transactions"
    CASE_SUBMISSIONS = "case_submissions"

    # Security metrics
    LOGIN_ATTEMPTS = "login_attempts"
    FAILED_LOGINS = "failed_logins"
    BLOCKED_IPS = "blocked_ips"
    SECURITY_VIOLATIONS = "security_violations"

    # System health
    UPTIME = "uptime"
    AVAILABILITY = "availability"
    DATABASE_CONNECTIONS = "database_connections"
    QUEUE_SIZE = "queue_size"


class MetricUnit(str, Enum):
    """Units for metrics."""

    COUNT = "count"
    PERCENTAGE = "percentage"
    MILLISECONDS = "milliseconds"
    SECONDS = "seconds"
    BYTES = "bytes"
    MEGABYTES = "megabytes"
    GIGABYTES = "gigabytes"
    REQUESTS_PER_SECOND = "requests_per_second"
    TRANSACTIONS_PER_MINUTE = "transactions_per_minute"


class MetricCategory(str, Enum):
    """Categories for organizing metrics."""

    PERFORMANCE = "performance"
    USAGE = "usage"
    BUSINESS = "business"
    SECURITY = "security"
    INFRASTRUCTURE = "infrastructure"
    APPLICATION = "application"


class SystemMetric(Base):
    """System metric model for tracking performance and usage statistics."""

    __tablename__ = "monitoring_system_metrics"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, index=True)

    # Metric identification
    metric_name = Column(String(100), nullable=False, index=True)
    metric_type = Column(SQLEnum(MetricType), nullable=False, index=True)
    category = Column(SQLEnum(MetricCategory), nullable=False, index=True)

    # Metric value and metadata
    value = Column(Float, nullable=False)
    unit = Column(SQLEnum(MetricUnit), nullable=False)

    # Context information
    module = Column(String(50), index=True)
    component = Column(String(100), index=True)
    environment = Column(String(20), default="production", index=True)

    # Geographic context
    province = Column(String(100), index=True)
    municipality = Column(String(100), index=True)

    # Time information
    timestamp = Column(DateTime, default=func.now(), nullable=False, index=True)
    collection_interval = Column(Integer)  # Seconds between collections

    # Additional data
    tags = Column(JSON)  # Key-value pairs for filtering
    meta_info = Column(JSON)  # Additional structured data

    # Aggregation information
    is_aggregated = Column(Boolean, default=False)
    aggregation_type = Column(String(20))  # sum, avg, min, max, count
    sample_count = Column(Integer)  # Number of samples in aggregation

    # Thresholds and alerts
    warning_threshold = Column(Float)
    critical_threshold = Column(Float)
    is_anomaly = Column(Boolean, default=False)

    def __repr__(self):
        return f"<SystemMetric(name={self.metric_name}, value={self.value}, unit={self.unit})>"

    @property
    def is_above_warning(self) -> bool:
        """Check if metric value is above warning threshold."""
        return (
            self.warning_threshold is not None and self.value > self.warning_threshold
        )

    @property
    def is_above_critical(self) -> bool:
        """Check if metric value is above critical threshold."""
        return (
            self.critical_threshold is not None and self.value > self.critical_threshold
        )

    @property
    def alert_level(self) -> Optional[str]:
        """Get alert level based on thresholds."""
        if self.is_above_critical:
            return "critical"
        elif self.is_above_warning:
            return "warning"
        return None

    def to_dict(self) -> Dict[str, Any]:
        """Convert metric to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "metric_name": self.metric_name,
            "metric_type": self.metric_type.value,
            "category": self.category.value,
            "value": self.value,
            "unit": self.unit.value,
            "module": self.module,
            "component": self.component,
            "environment": self.environment,
            "province": self.province,
            "municipality": self.municipality,
            "timestamp": self.timestamp.isoformat(),
            "collection_interval": self.collection_interval,
            "tags": self.tags,
            "meta_info": self.meta_info,
            "is_aggregated": self.is_aggregated,
            "aggregation_type": self.aggregation_type,
            "sample_count": self.sample_count,
            "warning_threshold": self.warning_threshold,
            "critical_threshold": self.critical_threshold,
            "is_anomaly": self.is_anomaly,
            "alert_level": self.alert_level,
        }

