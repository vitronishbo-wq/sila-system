# Dashboard Schemas - SILA System
# Fase 1: Módulos Críticos

from .dashboard_stats import (
    DashboardStatsResponse,
    DashboardStatsCreate,
    DashboardStatsUpdate,
)
from .system_health import SystemHealthResponse, SystemHealthCreate, SystemHealthUpdate
from .activity_log import (
    ActivityLogResponse,
    ActivityLogCreate,
    ActivityLogListResponse,
)

__all__ = [
    # Dashboard Stats
    "DashboardStatsResponse",
    "DashboardStatsCreate",
    "DashboardStatsUpdate",
    # System Health
    "SystemHealthResponse",
    "SystemHealthCreate",
    "SystemHealthUpdate",
    # Activity Log
    "ActivityLogResponse",
    "ActivityLogCreate",
    "ActivityLogListResponse",
]
