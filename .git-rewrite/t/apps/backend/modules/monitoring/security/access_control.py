# /opt/sila-system/backend/modules/monitoring/security/access_control.py

"""Access control for monitoring module operations."""

import enum
from datetime import datetime  # MOVEMOS ESTA IMPORTAÇÃO PARA O TOPO (BOA PRÁTICA)
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from app.schemas.user import User


class MonitoringRole(str, enum.Enum):
    """Monitoring-specific roles."""

    ADMIN = "admin"
    AUDITOR = "auditor"
    ANALYST = "analyst"
    VIEWER = "viewer"
    SYSTEM = "system"


class MonitoringPermission(str, enum.Enum):
    """Monitoring permissions."""

    # Audit log permissions
    VIEW_AUDIT_LOGS = "view_audit_logs"
    CREATE_AUDIT_LOGS = "create_audit_logs"
    VERIFY_AUDIT_INTEGRITY = "verify_audit_integrity"
    CLEANUP_AUDIT_LOGS = "cleanup_audit_logs"

    # Metric permissions
    VIEW_METRICS = "view_metrics"
    CREATE_METRICS = "create_metrics"
    UPDATE_METRIC_THRESHOLDS = "update_metric_thresholds"
    AGGREGATE_METRICS = "aggregate_metrics"
    CLEANUP_METRICS = "cleanup_metrics"

    # Alert permissions
    VIEW_ALERTS = "view_alerts"
    CREATE_ALERTS = "create_alerts"
    ACKNOWLEDGE_ALERTS = "acknowledge_alerts"
    RESOLVE_ALERTS = "resolve_alerts"
    SUPPRESS_ALERTS = "suppress_alerts"
    ESCALATE_ALERTS = "escalate_alerts"
    CLEANUP_ALERTS = "cleanup_alerts"

    # Dashboard permissions
    VIEW_DASHBOARD = "view_dashboard"
    VIEW_SYSTEM_STATUS = "view_system_status"
    VIEW_PERFORMANCE_METRICS = "view_performance_metrics"

    # Security permissions
    VIEW_SECURITY_EVENTS = "view_security_events"
    MANAGE_SECURITY_SETTINGS = "manage_security_settings"
    VIEW_SENSITIVE_DATA = "view_sensitive_data"

    # Administrative permissions
    MANAGE_MONITORING_CONFIG = "manage_monitoring_config"
    PERFORM_SYSTEM_OPERATIONS = "perform_system_operations"


class MonitoringAccessControl:
    """Access control service for monitoring operations."""

    def __init__(self, db: Session):
        self.db = db
        self.role_permissions = self._define_role_permissions()

    def check_permission(
        self,
        user: User,
        permission: MonitoringPermission,
        resource_context: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Check if user has specific monitoring permission."""
        # System users have all permissions
        if user.role == "system":
            return True

        # Get user's monitoring role
        monitoring_role = self._get_monitoring_role(user)

        # Check role-based permissions
        role_perms = self.role_permissions.get(monitoring_role, set())
        if permission not in role_perms:
            return False

        # Apply additional context-based restrictions
        return self._check_context_restrictions(user, permission, resource_context)

    def require_permission(
        self,
        user: User,
        permission: MonitoringPermission,
        resource_context: Optional[Dict[str, Any]] = None,
    ):
        """Require specific permission or raise exception."""
        if not self.check_permission(user, permission, resource_context):
            raise PermissionError(
                f"User {user.email} does not have permission: {permission.value}"
            )

    def get_user_permissions(self, user: User) -> List[MonitoringPermission]:
        """Get all permissions for a user."""
        monitoring_role = self._get_monitoring_role(user)
        return list(self.role_permissions.get(monitoring_role, set()))

    def can_view_audit_log(self, user: User, audit_log_data: Dict[str, Any]) -> bool:
        """Check if user can view specific audit log."""
        if not self.check_permission(user, MonitoringPermission.VIEW_AUDIT_LOGS):
            return False

        # Additional restrictions for sensitive audit logs
        if audit_log_data.get("level") == "critical":
            return self.check_permission(
                user, MonitoringPermission.VIEW_SECURITY_EVENTS
            )

        # Users can always view their own audit logs
        if audit_log_data.get("user_id") == user.id:
            return True

        return True

    def can_view_metric(self, user: User, metric_data: Dict[str, Any]) -> bool:
        """Check if user can view specific metric."""
        if not self.check_permission(user, MonitoringPermission.VIEW_METRICS):
            return False

        # Check for sensitive metrics
        sensitive_metrics = [
            "security_violations",
            "failed_logins",
            "unauthorized_access",
        ]

        if metric_data.get("metric_name") in sensitive_metrics:
            return self.check_permission(
                user, MonitoringPermission.VIEW_SECURITY_EVENTS
            )

        return True

    def can_view_alert(self, user: User, alert_data: Dict[str, Any]) -> bool:
        """Check if user can view specific alert."""
        if not self.check_permission(user, MonitoringPermission.VIEW_ALERTS):
            return False

        # Security alerts require special permission
        if alert_data.get("category") == "security":
            return self.check_permission(
                user, MonitoringPermission.VIEW_SECURITY_EVENTS
            )

        return True

    def can_modify_alert(
        self, user: User, alert_data: Dict[str, Any], action: str
    ) -> bool:
        """Check if user can modify specific alert."""
        # Map actions to permissions
        action_permissions = {
            "acknowledge": MonitoringPermission.ACKNOWLEDGE_ALERTS,
            "resolve": MonitoringPermission.RESOLVE_ALERTS,
            "suppress": MonitoringPermission.SUPPRESS_ALERTS,
            "escalate": MonitoringPermission.ESCALATE_ALERTS,
        }

        required_permission = action_permissions.get(action)
        if not required_permission:
            return False

        if not self.check_permission(user, required_permission):
            return False

        # Critical alerts require admin permission for suppression
        if (
            action == "suppress"
            and alert_data.get("severity") == "critical"
            and not self._is_admin(user)
        ):
            return False

        return True

    def filter_audit_logs_by_access(
        self, user: User, audit_logs: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Filter audit logs based on user access permissions."""
        if self._is_admin(user) or self._is_auditor(user):
            return audit_logs

        # Filter logs user can access
        accessible_logs = []
        for log in audit_logs:
            if self.can_view_audit_log(user, log):
                # Mask sensitive data for non-privileged users
                if not self.check_permission(
                    user, MonitoringPermission.VIEW_SENSITIVE_DATA
                ):
                    log = self._mask_sensitive_audit_data(log)
                accessible_logs.append(log)

        return accessible_logs

    def filter_metrics_by_access(
        self, user: User, metrics: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Filter metrics based on user access permissions."""
        accessible_metrics = []

        for metric in metrics:
            if self.can_view_metric(user, metric):
                accessible_metrics.append(metric)

        return accessible_metrics

    def filter_alerts_by_access(
        self, user: User, alerts: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Filter alerts based on user access permissions."""
        accessible_alerts = []

        for alert in alerts:
            if self.can_view_alert(user, alert):
                accessible_alerts.append(alert)

        return accessible_alerts

    def get_geographic_restrictions(self, user: User) -> Optional[Dict[str, List[str]]]:
        """Get geographic restrictions for user."""
        # Admin and system users have no geographic restrictions
        if self._is_admin(user) or user.role == "system":
            return None

        # Get user's geographic scope from profile
        user_province = getattr(user, "province", None)
        user_municipality = getattr(user, "municipality", None)

        if user_province:
            restrictions = {"provinces": [user_province]}
            if user_municipality:
                restrictions["municipalities"] = [user_municipality]
            return restrictions

        return None

    def apply_geographic_filters(
        self, user: User, query_filters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply geographic filters to query based on user restrictions."""
        restrictions = self.get_geographic_restrictions(user)

        if restrictions:
            if "provinces" in restrictions and not query_filters.get("province"):
                query_filters["province"] = restrictions["provinces"][0]

            if "municipalities" in restrictions and not query_filters.get(
                "municipality"
            ):
                query_filters["municipality"] = restrictions["municipalities"][0]

        return query_filters

    # ============================================================================
    # PRIVATE HELPER METHODS
    # ============================================================================

    def _define_role_permissions(self) -> Dict[MonitoringRole, set]:
        """Define permissions for each monitoring role."""
        return {
            MonitoringRole.ADMIN: {
                # All permissions
                MonitoringPermission.VIEW_AUDIT_LOGS,
                MonitoringPermission.CREATE_AUDIT_LOGS,
                MonitoringPermission.VERIFY_AUDIT_INTEGRITY,
                MonitoringPermission.CLEANUP_AUDIT_LOGS,
                MonitoringPermission.VIEW_METRICS,
                MonitoringPermission.CREATE_METRICS,
                MonitoringPermission.UPDATE_METRIC_THRESHOLDS,
                MonitoringPermission.AGGREGATE_METRICS,
                MonitoringPermission.CLEANUP_METRICS,
                MonitoringPermission.VIEW_ALERTS,
                MonitoringPermission.CREATE_ALERTS,
                MonitoringPermission.ACKNOWLEDGE_ALERTS,
                MonitoringPermission.RESOLVE_ALERTS,
                MonitoringPermission.SUPPRESS_ALERTS,
                MonitoringPermission.ESCALATE_ALERTS,
                MonitoringPermission.CLEANUP_ALERTS,
                MonitoringPermission.VIEW_DASHBOARD,
                MonitoringPermission.VIEW_SYSTEM_STATUS,
                MonitoringPermission.VIEW_PERFORMANCE_METRICS,
                MonitoringPermission.VIEW_SECURITY_EVENTS,
                MonitoringPermission.MANAGE_SECURITY_SETTINGS,
                MonitoringPermission.VIEW_SENSITIVE_DATA,
                MonitoringPermission.MANAGE_MONITORING_CONFIG,
                MonitoringPermission.PERFORM_SYSTEM_OPERATIONS,
            },
            MonitoringRole.AUDITOR: {
                MonitoringPermission.VIEW_AUDIT_LOGS,
                MonitoringPermission.CREATE_AUDIT_LOGS,
                MonitoringPermission.VERIFY_AUDIT_INTEGRITY,
                MonitoringPermission.VIEW_METRICS,
                MonitoringPermission.AGGREGATE_METRICS,
                MonitoringPermission.VIEW_ALERTS,
                MonitoringPermission.VIEW_DASHBOARD,
                MonitoringPermission.VIEW_SYSTEM_STATUS,
                MonitoringPermission.VIEW_PERFORMANCE_METRICS,
                MonitoringPermission.VIEW_SECURITY_EVENTS,
                MonitoringPermission.VIEW_SENSITIVE_DATA,
            },
            MonitoringRole.ANALYST: {
                MonitoringPermission.VIEW_AUDIT_LOGS,
                MonitoringPermission.VIEW_METRICS,
                MonitoringPermission.UPDATE_METRIC_THRESHOLDS,
                MonitoringPermission.AGGREGATE_METRICS,
                MonitoringPermission.VIEW_ALERTS,
                MonitoringPermission.ACKNOWLEDGE_ALERTS,
                MonitoringPermission.RESOLVE_ALERTS,
                MonitoringPermission.VIEW_DASHBOARD,
                MonitoringPermission.VIEW_SYSTEM_STATUS,
                MonitoringPermission.VIEW_PERFORMANCE_METRICS,
            },
            MonitoringRole.VIEWER: {
                MonitoringPermission.VIEW_AUDIT_LOGS,
                MonitoringPermission.VIEW_METRICS,
                MonitoringPermission.VIEW_ALERTS,
                MonitoringPermission.VIEW_DASHBOARD,
                MonitoringPermission.VIEW_SYSTEM_STATUS,
                MonitoringPermission.VIEW_PERFORMANCE_METRICS,
            },
            MonitoringRole.SYSTEM: {
                # System role gets all permissions
                MonitoringPermission.VIEW_AUDIT_LOGS,
                MonitoringPermission.CREATE_AUDIT_LOGS,
                MonitoringPermission.VERIFY_AUDIT_INTEGRITY,
                MonitoringPermission.CLEANUP_AUDIT_LOGS,
                MonitoringPermission.VIEW_METRICS,
                MonitoringPermission.CREATE_METRICS,
                MonitoringPermission.UPDATE_METRIC_THRESHOLDS,
                MonitoringPermission.AGGREGATE_METRICS,
                MonitoringPermission.CLEANUP_METRICS,
                MonitoringPermission.VIEW_ALERTS,
                MonitoringPermission.CREATE_ALERTS,
                MonitoringPermission.ACKNOWLEDGE_ALERTS,
                MonitoringPermission.RESOLVE_ALERTS,
                MonitoringPermission.SUPPRESS_ALERTS,
                MonitoringPermission.ESCALATE_ALERTS,
                MonitoringPermission.CLEANUP_ALERTS,
                MonitoringPermission.VIEW_DASHBOARD,
                MonitoringPermission.VIEW_SYSTEM_STATUS,
                MonitoringPermission.VIEW_PERFORMANCE_METRICS,
                MonitoringPermission.VIEW_SECURITY_EVENTS,
                MonitoringPermission.MANAGE_SECURITY_SETTINGS,
                MonitoringPermission.VIEW_SENSITIVE_DATA,
                MonitoringPermission.MANAGE_MONITORING_CONFIG,
                MonitoringPermission.PERFORM_SYSTEM_OPERATIONS,
            },
        }

    def _get_monitoring_role(self, user: User) -> MonitoringRole:
        """Get monitoring role for user."""
        # Map system roles to monitoring roles
        role_mapping = {
            "admin": MonitoringRole.ADMIN,
            "auditor": MonitoringRole.AUDITOR,
            "analyst": MonitoringRole.ANALYST,
            "system": MonitoringRole.SYSTEM,
        }

        return role_mapping.get(user.role, MonitoringRole.VIEWER)

    def _check_context_restrictions(
        self,
        user: User,
        permission: MonitoringPermission,
        resource_context: Optional[Dict[str, Any]],
    ) -> bool:
        """Apply additional context-based restrictions."""
        if not resource_context:
            return True

        # Time-based restrictions
        if resource_context.get("time_restricted"):
            # Some operations only allowed during business hours
            # datetime is now imported at the top of the file
            current_hour = datetime.now().hour
            if not (8 <= current_hour <= 18):  # 8 AM to 6 PM
                return self._is_admin(user)

        # Data sensitivity restrictions
        if resource_context.get("sensitivity_level") == "restricted":
            return self.check_permission(user, MonitoringPermission.VIEW_SENSITIVE_DATA)

        # Module-specific restrictions
        restricted_modules = resource_context.get("restricted_modules", [])
        if restricted_modules and not self._is_admin(user):
            user_modules = getattr(user, "allowed_modules", [])
            if not any(module in user_modules for module in restricted_modules):
                return False

        return True

    def _is_admin(self, user: User) -> bool:
        """Check if user is admin."""
        return user.role == "admin"

    def _is_auditor(self, user: User) -> bool:
        """Check if user is auditor."""
        return user.role in ["admin", "auditor"]

    def _mask_sensitive_audit_data(self, audit_log: Dict[str, Any]) -> Dict[str, Any]:
        """Mask sensitive data in audit log for non-privileged users."""
        masked_log = audit_log.copy()

        # Mask sensitive fields
        sensitive_fields = ["ip_address", "session_id", "user_agent"]
        for field in sensitive_fields:
            if field in masked_log and masked_log[field]:
                masked_log[field] = "***MASKED***"

        # Partially mask email
        if "user_email" in masked_log and masked_log["user_email"]:
            email = masked_log["user_email"]
            if "@" in email:
                username, domain = email.split("@", 1)
                masked_username = username[:2] + "*" * (len(username) - 2)
                masked_log["user_email"] = f"{masked_username}@{domain}"

        return masked_log
