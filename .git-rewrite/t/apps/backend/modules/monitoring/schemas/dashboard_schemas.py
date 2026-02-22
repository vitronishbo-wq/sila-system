"""
Dashboard-related Pydantic schemas for API responses
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict


class MonitoringDashboard(BaseModel):
    """Schema for monitoring dashboard data."""

    system_health: Dict[str, Any]
    alert_summary: Dict[str, int]
    recent_alerts: List[Dict[str, Any]]
    metric_summary: Dict[str, Any]
    performance_metrics: Dict[str, float]
    audit_summary: Dict[str, int]
    top_issues: List[Dict[str, Any]]
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)


class DashboardWidget(BaseModel):
    """Schema for individual dashboard widget."""

    widget_id: str
    widget_type: str
    title: str
    data: Dict[str, Any]
    last_updated: datetime
    refresh_interval_seconds: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
