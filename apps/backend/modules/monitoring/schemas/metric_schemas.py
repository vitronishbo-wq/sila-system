"""
Metric-related Pydantic schemas for API requests/responses
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class SystemMetricCreate(BaseModel):
    """Schema for creating a system metric."""

    metric_name: str = Field(..., max_length=100)
    metric_type: str
    metric_unit: str
    metric_category: str
    value: float
    source_module: Optional[str] = Field(None, max_length=50)
    source_component: Optional[str] = Field(None, max_length=100)
    province: Optional[str] = Field(None, max_length=100)
    municipality: Optional[str] = Field(None, max_length=100)
    metadata: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None

    model_config = ConfigDict(from_attributes=True)


class SystemMetricFilter(BaseModel):
    """Schema for filtering system metrics."""

    metric_name: Optional[str] = None
    metric_type: Optional[str] = None
    metric_category: Optional[str] = None
    source_module: Optional[str] = None
    province: Optional[str] = None
    municipality: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    limit: int = Field(100, ge=1, le=5000)
    offset: int = Field(0, ge=0)

    model_config = ConfigDict(from_attributes=True)


class SystemMetricUpdate(BaseModel):
    """Schema for updating a system metric."""

    value: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None

    model_config = ConfigDict(from_attributes=True)


class SystemMetricResponse(BaseModel):
    """Schema for system metric response."""

    id: int
    metric_name: str
    metric_type: str
    metric_unit: str
    metric_category: str
    value: float
    source_module: Optional[str] = None
    source_component: Optional[str] = None
    timestamp: datetime
    province: Optional[str] = None
    municipality: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None

    model_config = ConfigDict(from_attributes=True)


class MetricAggregation(BaseModel):
    """Schema for metric aggregation results."""

    metric_name: str
    aggregation_type: str = Field(..., description="Type: avg, sum, min, max, count")
    value: float
    start_date: datetime
    end_date: datetime
    count: int
    metadata: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(from_attributes=True)


class SystemHealthStatus(BaseModel):
    """Schema for system health status."""

    status: str = Field(..., description="Overall health: healthy, degraded, critical")
    cpu_usage_percent: Optional[float] = None
    memory_usage_percent: Optional[float] = None
    disk_usage_percent: Optional[float] = None
    active_alerts: int
    critical_alerts: int
    services_status: Dict[str, str]
    last_check: datetime
    uptime_seconds: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)
