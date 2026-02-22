"""Pydantic schemas for monitoring module with CRUD support."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from modules.monitoring.models.alert import (
    AlertCategory,
    AlertSeverity,
    AlertStatus,
    AlertType,
)


# Alert schemas
class AlertBase(BaseModel):
    """Base schema for system alerts."""

    alert_type: AlertType = Field(..., description="Type of alert")
    severity: AlertSeverity = Field(..., description="Alert severity level")
    category: AlertCategory = Field(..., description="Alert category")
    title: str = Field(..., max_length=200, description="Alert title")
    description: str = Field(..., description="Alert description")
    source: str = Field(..., description="Alert source system/module")
    entity_id: Optional[str] = Field(None, description="Related entity ID")
    entity_type: Optional[str] = Field(None, description="Related entity type")
    metadata: Optional[Dict[str, Any]] = Field(
        default_factory=dict, description="Additional alert data"
    )


class AlertCreate(AlertBase):
    """Schema for creating alert."""


class AlertUpdate(BaseModel):
    """Schema for updating alert."""

    severity: Optional[AlertSeverity] = None
    status: Optional[AlertStatus] = None
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    acknowledged_by: Optional[str] = None
    acknowledged_at: Optional[datetime] = None
    resolved_by: Optional[str] = None
    resolved_at: Optional[datetime] = None
    resolution_notes: Optional[str] = None
    escalated_to: Optional[str] = None
    escalated_at: Optional[datetime] = None
    escalation_reason: Optional[str] = None


class AlertInDB(AlertBase):
    """Schema for alert as stored in database."""

    id: int
    status: AlertStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    acknowledged_by: Optional[str] = None
    acknowledged_at: Optional[datetime] = None
    resolved_by: Optional[str] = None
    resolved_at: Optional[datetime] = None
    resolution_notes: Optional[str] = None
    escalated_to: Optional[str] = None
    escalated_at: Optional[datetime] = None
    escalation_reason: Optional[str] = None

    class Config:
        from_attributes = True


class AlertOut(AlertInDB):
    """Schema for alert output."""


class AlertFilter(BaseModel):
    """Schema for filtering alerts."""

    alert_type: Optional[AlertType] = None
    severity: Optional[AlertSeverity] = None
    category: Optional[AlertCategory] = None
    status: Optional[AlertStatus] = None
    source: Optional[str] = None
    title: Optional[str] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    skip: Optional[int] = Field(0, ge=0)
    limit: Optional[int] = Field(100, ge=1, le=1000)


# System Metric schemas
class SystemMetricBase(BaseModel):
    """Base schema for system metrics."""

    metric_type: str = Field(..., description="Type of metric")
    metric_name: str = Field(..., description="Name of metric")
    value: float = Field(..., description="Metric value")
    unit: str = Field(..., description="Unit of measurement")
    source: str = Field(..., description="Metric source")
    tags: Optional[Dict[str, str]] = Field(
        default_factory=dict, description="Metric tags"
    )


class SystemMetricCreate(SystemMetricBase):
    """Schema for creating system metric."""


class SystemMetricInDB(SystemMetricBase):
    """Schema for system metric as stored in database."""

    id: int
    timestamp: datetime

    class Config:
        from_attributes = True


class SystemMetricOut(SystemMetricInDB):
    """Schema for system metric output."""


# Audit Log schemas
class AuditLogBase(BaseModel):
    """Base schema for audit logs."""

    user_id: str = Field(..., description="User who performed action")
    action: str = Field(..., description="Action performed")
    resource_type: str = Field(..., description="Type of resource")
    resource_id: Optional[str] = Field(None, description="Resource ID")
    details: Optional[Dict[str, Any]] = Field(
        default_factory=dict, description="Action details"
    )
    ip_address: Optional[str] = Field(None, description="User IP address")
    user_agent: Optional[str] = Field(None, description="User agent string")


class AuditLogCreate(AuditLogBase):
    """Schema for creating audit log."""


class AuditLogInDB(AuditLogBase):
    """Schema for audit log as stored in database."""

    id: int
    timestamp: datetime

    class Config:
        from_attributes = True


class AuditLogOut(AuditLogInDB):
    """Schema for audit log output."""


# Statistics and Analytics schemas
class AlertStatistics(BaseModel):
    """Schema for alert statistics."""

    total_alerts: int
    unique_types: int
    severity_breakdown: Dict[str, int]
    category_breakdown: Dict[str, int]
    period_hours: int
    last_updated: datetime


class SystemMetricsSummary(BaseModel):
    """Schema for system metrics summary."""

    metric_type: str
    current_value: float
    average_value: float
    min_value: float
    max_value: float
    trend: str  # "increasing", "decreasing", "stable"
    period_minutes: int


class MonitoringDashboard(BaseModel):
    """Schema for monitoring dashboard data."""

    active_alerts: List[AlertOut]
    critical_alerts: List[AlertOut]
    recent_metrics: List[SystemMetricOut]
    alert_statistics: AlertStatistics
    system_health: Dict[str, Any]
    last_updated: datetime


# Alert Management schemas
class AlertAcknowledgeRequest(BaseModel):
    """Schema for acknowledging alert."""

    alert_id: int
    acknowledged_by: str
    notes: Optional[str] = None


class AlertResolveRequest(BaseModel):
    """Schema for resolving alert."""

    alert_id: int
    resolved_by: str
    resolution_notes: Optional[str] = None


class AlertEscalateRequest(BaseModel):
    """Schema for escalating alert."""

    alert_id: int
    escalated_to: str
    escalation_reason: str


class AlertBatchOperation(BaseModel):
    """Schema for batch alert operations."""

    alert_ids: List[int] = Field(..., min_items=1, max_items=100)
    operation: str = Field(..., regex="^(acknowledge|resolve|escalate|suppress)$")
    performed_by: str
    notes: Optional[str] = None


# Monitoring Configuration schemas
class AlertRuleBase(BaseModel):
    """Base schema for alert rules."""

    name: str = Field(..., description="Rule name")
    description: str = Field(..., description="Rule description")
    alert_type: AlertType = Field(..., description="Alert type to trigger")
    severity: AlertSeverity = Field(..., description="Alert severity")
    condition: str = Field(..., description="Alert condition expression")
    threshold: float = Field(..., description="Alert threshold")
    time_window_minutes: int = Field(
        ..., ge=1, description="Time window for evaluation"
    )
    is_active: bool = Field(default=True, description="Rule active status")


class AlertRuleCreate(AlertRuleBase):
    """Schema for creating alert rule."""


class AlertRuleOut(AlertRuleBase):
    """Schema for alert rule output."""

    id: int
    created_at: datetime
    last_triggered: Optional[datetime] = None
    trigger_count: int = 0

    class Config:
        from_attributes = True


# Notification schemas
class AlertNotificationBase(BaseModel):
    """Base schema for alert notifications."""

    alert_id: int
    channel: str = Field(..., regex="^(email|sms|slack|webhook|push)$")
    recipient: str = Field(..., description="Notification recipient")
    message: str = Field(..., description="Notification message")
    status: str = Field(default="pending", regex="^(pending|sent|failed|retry)$")


class AlertNotificationCreate(AlertNotificationBase):
    """Schema for creating alert notification."""


class AlertNotificationOut(AlertNotificationBase):
    """Schema for alert notification output."""

    id: int
    sent_at: Optional[datetime] = None
    error_message: Optional[str] = None
    retry_count: int = 0

    class Config:
        from_attributes = True


# Response schemas
class MonitoringListResponse(BaseModel):
    """Schema for paginated list response."""

    items: List[Dict[str, Any]]
    total: int
    skip: int
    limit: int
    has_next: bool
    has_prev: bool


class MonitoringBatchResponse(BaseModel):
    """Schema for batch operation response."""

    successful: List[Dict[str, Any]]
    failed: List[Dict[str, Any]]
    total_attempted: int
    total_successful: int
    total_failed: int


# Health Check schemas
class HealthCheckResult(BaseModel):
    """Schema for health check results."""

    service_name: str
    status: str = Field(..., regex="^(healthy|unhealthy|degraded)$")
    response_time_ms: float
    last_check: datetime
    error_message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class SystemHealth(BaseModel):
    """Schema for overall system health."""

    overall_status: str = Field(..., regex="^(healthy|unhealthy|degraded)$")
    services: List[HealthCheckResult]
    active_alerts_count: int
    critical_alerts_count: int
    uptime_percentage: float
    last_updated: datetime


# Export all schemas
__all__ = [
    # Alert schemas
    "AlertBase",
    "AlertCreate",
    "AlertUpdate",
    "AlertInDB",
    "AlertOut",
    "AlertFilter",
    # System Metric schemas
    "SystemMetricBase",
    "SystemMetricCreate",
    "SystemMetricInDB",
    "SystemMetricOut",
    # Audit Log schemas
    "AuditLogBase",
    "AuditLogCreate",
    "AuditLogInDB",
    "AuditLogOut",
    # Statistics schemas
    "AlertStatistics",
    "SystemMetricsSummary",
    "MonitoringDashboard",
    # Alert Management schemas
    "AlertAcknowledgeRequest",
    "AlertResolveRequest",
    "AlertEscalateRequest",
    "AlertBatchOperation",
    # Configuration schemas
    "AlertRuleBase",
    "AlertRuleCreate",
    "AlertRuleOut",
    # Notification schemas
    "AlertNotificationBase",
    "AlertNotificationCreate",
    "AlertNotificationOut",
    # Response schemas
    "MonitoringListResponse",
    "MonitoringBatchResponse",
    # Health Check schemas
    "HealthCheckResult",
    "SystemHealth",
]
