"""
Audit module - Consolidated
Exposes: AuditLog model, audit_log function, AuditAnalytics, SLA definitions.
"""

from app.core.audit_legacy import AuditLog, audit_log, ImmutableAuditLog
from app.core.audit.analytics import AuditAnalytics
from app.core.audit.sla_definitions import (
    SLA_DEFINITIONS,
    SLO_TARGETS,
    ANOMALY_THRESHOLDS,
    get_sla_for_service,
    evaluate_sla_status,
)

__all__ = [
    "AuditLog",
    "audit_log",
    "ImmutableAuditLog",
    "AuditAnalytics",
    "SLA_DEFINITIONS",
    "SLO_TARGETS",
    "ANOMALY_THRESHOLDS",
    "get_sla_for_service",
    "evaluate_sla_status",
]
