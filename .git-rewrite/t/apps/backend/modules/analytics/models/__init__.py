"""
Módulo de modelos para analytics.
"""

from .analytics_models import (
    Metric,
    MetricValue,
    Dashboard,
    DashboardMetric,
    DashboardAccessLog,
    Report,
    ReportExecution,
    AlertRule,
    Alert,
    ScheduledReport,
    ScheduledReportExecution,
    AnalyticsCache,
)

__all__ = [
    "Metric",
    "MetricValue",
    "Dashboard",
    "DashboardMetric",
    "DashboardAccessLog",
    "Report",
    "ReportExecution",
    "AlertRule",
    "Alert",
    "ScheduledReport",
    "ScheduledReportExecution",
    "AnalyticsCache",
]
