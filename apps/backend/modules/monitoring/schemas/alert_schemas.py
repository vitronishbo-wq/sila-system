"""
Alert-related Pydantic schemas for API requests/responses
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field

try:
    from .alert import AlertSeverity, AlertStatus, AlertType
except ImportError:
    from alert import AlertSeverity, AlertStatus, AlertType


class AlertCreate(BaseModel):
    """Schema for creating a new alert."""

    alert_type: AlertType
    severity: AlertSeverity
    category: Optional[str] = None
    title: str
    description: str
    recommendation: Optional[str] = None
    source_module: Optional[str] = None
    source_component: Optional[str] = None
    source_metric_id: Optional[int] = None
    affected_resource_type: Optional[str] = None
    affected_resource_id: Optional[int] = None
    affected_users_count: Optional[int] = None
    province: Optional[str] = None
    municipality: Optional[str] = None
    trigger_conditions: Optional[Dict[str, Any]] = None
    alert_data: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None
    notification_channels: Optional[List[str]] = None
    group_key: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class AlertUpdate(BaseModel):
    """Schema for updating an alert."""

    severity: Optional[AlertSeverity] = None
    status: Optional[AlertStatus] = None
    recommendation: Optional[str] = None
    resolution_notes: Optional[str] = None
    tags: Optional[List[str]] = None
    is_suppressed: Optional[bool] = None
    suppressed_until: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class AlertResolve(BaseModel):
    """Schema for resolving an alert."""

    resolution_notes: str = Field(
        ..., description="Notes about how the alert was resolved"
    )
    resolved_by: Optional[int] = Field(
        None, description="User ID who resolved the alert"
    )

    model_config = ConfigDict(from_attributes=True)


class AlertFilter(BaseModel):
    """Schema for filtering alerts."""

    alert_type: Optional[AlertType] = None
    severity: Optional[AlertSeverity] = None
    status: Optional[AlertStatus] = None
    source_module: Optional[str] = None
    province: Optional[str] = None
    municipality: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_critical: Optional[bool] = None
    is_active: Optional[bool] = None
    limit: int = Field(100, ge=1, le=1000)
    offset: int = Field(0, ge=0)

    model_config = ConfigDict(from_attributes=True)


class AlertResponse(BaseModel):
    """Schema for alert response."""

    id: int
    alert_type: AlertType
    severity: AlertSeverity
    status: AlertStatus
    title: str
    description: str
    recommendation: Optional[str] = None
    source_module: Optional[str] = None
    created_at: datetime
    acknowledged_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    is_active: bool
    is_critical: bool
    duration_minutes: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class AlertStatistics(BaseModel):
    """Schema for alert statistics."""

    total_alerts: int
    active_alerts: int
    critical_alerts: int
    high_severity_alerts: int
    resolved_today: int
    average_resolution_time_minutes: Optional[float] = None
    alerts_by_severity: Dict[str, int]
    alerts_by_type: Dict[str, int]
    alerts_by_module: Dict[str, int]

    model_config = ConfigDict(from_attributes=True)
