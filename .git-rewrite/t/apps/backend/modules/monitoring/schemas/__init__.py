"""
Schemas for Monitoring module.
Central place for Pydantic models & enums like Alerts, Audit logs, etc.
"""

# Base alert enums and schemas
from .alert import AlertSchema, AlertAcknowledge, AlertSeverity, AlertStatus, AlertType

# Alert CRUD schemas
from .alert_schemas import (
    AlertCreate,
    AlertUpdate,
    AlertResolve,
    AlertFilter,
    AlertResponse,
    AlertStatistics,
)

# Metric schemas
from .metric_schemas import (
    SystemMetricCreate,
    SystemMetricUpdate,
    SystemMetricFilter,
    SystemMetricResponse,
    MetricAggregation,
    SystemHealthStatus,
)

# Audit schemas
from .audit_schemas import (
    AuditLogCreate,
    AuditLogFilter,
    AuditLogResponse,
)

# Dashboard schemas
from .dashboard_schemas import (
    MonitoringDashboard,
    DashboardWidget,
)

__all__ = [
    # Alert base
    "AlertSchema",
    "AlertAcknowledge",
    "AlertSeverity",
    "AlertStatus",
    "AlertType",
    # Alert CRUD
    "AlertCreate",
    "AlertUpdate",
    "AlertResolve",
    "AlertFilter",
    "AlertResponse",
    "AlertStatistics",
    # Metrics
    "SystemMetricCreate",
    "SystemMetricUpdate",
    "SystemMetricFilter",
    "SystemMetricResponse",
    "MetricAggregation",
    "SystemHealthStatus",
    # Audit
    "AuditLogCreate",
    "AuditLogFilter",
    "AuditLogResponse",
    # Dashboard
    "MonitoringDashboard",
    "DashboardWidget",
]
