"""Security monitoring integration for the monitoring module."""

from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from sqlalchemy.orm import Session

from ..models.alert import AlertCategory, AlertSeverity, AlertType
from ..models.audit_log import AuditAction, AuditLevel
from ..services.alert_service import AlertService
from ..services.audit_service import AuditService


class SecurityMonitor:
    """Security monitoring service for detecting and alerting on security events."""

    def __init__(self, db: Session):
        self.db = db
        self.audit_service = AuditService(db)
        self.alert_service = AlertService(db)

    def monitor_login_attempts(
        self,
        user_id: Optional[int],
        user_email: str,
        ip_address: str,
        user_agent: str,
        success: bool,
        failure_reason: Optional[str] = None,
    ):
        """Monitor login attempts and detect suspicious patterns."""
        # Log the login attempt
        self.audit_service.log_user_action(
            user_id=user_id,
            user_email=user_email,
            user_role=None,
            action=AuditAction.LOGIN,
            module="auth",
            description=f"Login attempt {'successful' if success else 'failed'}",
            ip_address=ip_address,
            user_agent=user_agent,
            success=success,
            error_message=failure_reason,
            additional_data={"login_attempt": True, "failure_reason": failure_reason},
        )

        # Check for suspicious patterns if login failed
        if not success:
            self._check_failed_login_patterns(user_email, ip_address)

    def monitor_access_attempts(
        self,
        user_id: int,
        user_email: str,
        resource_type: str,
        resource_id: int,
        action: str,
        success: bool,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        denial_reason: Optional[str] = None,
    ):
        """Monitor resource access attempts and detect unauthorized access."""
        # Log the access attempt
        audit_action = AuditAction.ACCESS_DENIED if not success else AuditAction.READ

        self.audit_service.log_user_action(
            user_id=user_id,
            user_email=user_email,
            user_role=None,
            action=audit_action,
            module="auth",
            description=f"Access attempt to {resource_type} {resource_id}: {action}",
            resource_type=resource_type,
            resource_id=resource_id,
            ip_address=ip_address,
            user_agent=user_agent,
            success=success,
            error_message=denial_reason,
            additional_data={
                "access_attempt": True,
                "attempted_action": action,
                "denial_reason": denial_reason,
            },
        )

        # Check for suspicious access patterns if denied
        if not success:
            self._check_unauthorized_access_patterns(
                user_id, user_email, resource_type, ip_address
            )

    def monitor_data_access(
        self,
        user_id: int,
        user_email: str,
        data_type: str,
        data_sensitivity: str,  # "public", "internal", "confidential", "restricted"
        operation: str,  # "read", "create", "update", "delete"
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        additional_context: Optional[Dict[str, Any]] = None,
    ):
        """Monitor access to sensitive data."""
        # Determine audit level based on data sensitivity
        if data_sensitivity in ["confidential", "restricted"]:
            level = AuditLevel.WARNING
        elif data_sensitivity == "internal":
            level = AuditLevel.INFO
        else:
            level = AuditLevel.INFO

        # Log data access
        self.audit_service.log_user_action(
            user_id=user_id,
            user_email=user_email,
            user_role=None,
            action=self._operation_to_audit_action(operation),
            module="security",
            description=f"Data access: {operation} on {data_sensitivity} {data_type}",
            resource_type=data_type,
            ip_address=ip_address,
            user_agent=user_agent,
            success=True,
            additional_data={
                "data_access": True,
                "data_sensitivity": data_sensitivity,
                "operation": operation,
                **(additional_context or {}),
            },
        )

        # Check for unusual data access patterns
        if data_sensitivity in ["confidential", "restricted"]:
            self._check_sensitive_data_access_patterns(
                user_id, data_type, data_sensitivity
            )

    def monitor_privilege_escalation(
        self,
        user_id: int,
        user_email: str,
        old_role: str,
        new_role: str,
        changed_by_user_id: int,
        ip_address: Optional[str] = None,
        justification: Optional[str] = None,
    ):
        """Monitor privilege escalation events."""
        # Log privilege change
        self.audit_service.log_user_action(
            user_id=changed_by_user_id,
            user_email=None,
            user_role=None,
            action=AuditAction.UPDATE,
            module="auth",
            description=f"Privilege escalation: {user_email} from {old_role} to {new_role}",
            resource_type="user_role",
            resource_id=user_id,
            ip_address=ip_address,
            success=True,
            additional_data={
                "privilege_escalation": True,
                "target_user_id": user_id,
                "target_user_email": user_email,
                "old_role": old_role,
                "new_role": new_role,
                "justification": justification,
            },
        )

        # Create alert for privilege escalation
        self._create_privilege_escalation_alert(
            user_email, old_role, new_role, changed_by_user_id
        )

    def monitor_system_configuration_changes(
        self,
        user_id: int,
        user_email: str,
        configuration_type: str,
        old_value: Any,
        new_value: Any,
        ip_address: Optional[str] = None,
        justification: Optional[str] = None,
    ):
        """Monitor critical system configuration changes."""
        # Log configuration change
        self.audit_service.log_user_action(
            user_id=user_id,
            user_email=user_email,
            user_role=None,
            action=AuditAction.UPDATE,
            module="system",
            description=f"System configuration change: {configuration_type}",
            resource_type="system_config",
            ip_address=ip_address,
            success=True,
            additional_data={
                "configuration_change": True,
                "configuration_type": configuration_type,
                "old_value": str(old_value),
                "new_value": str(new_value),
                "justification": justification,
            },
        )

        # Create alert for critical configuration changes
        if self._is_critical_configuration(configuration_type):
            self._create_configuration_change_alert(configuration_type, user_email)

    def detect_anomalous_behavior(
        self,
        user_id: int,
        user_email: str,
        behavior_type: str,
        behavior_data: Dict[str, Any],
        anomaly_score: float,  # 0.0 to 1.0, where 1.0 is highly anomalous
        ip_address: Optional[str] = None,
    ):
        """Detect and report anomalous user behavior."""
        # Log anomalous behavior
        self.audit_service.log_security_event(
            event_type="anomalous_behavior",
            description=f"Anomalous behavior detected: {behavior_type} (score: {anomaly_score:.2f})",
            user_id=user_id,
            user_email=user_email,
            ip_address=ip_address,
            severity=AuditLevel.WARNING if anomaly_score > 0.7 else AuditLevel.INFO,
            additional_data={
                "behavior_type": behavior_type,
                "anomaly_score": anomaly_score,
                "behavior_data": behavior_data,
            },
        )

        # Create alert for high-risk anomalies
        if anomaly_score > 0.8:
            self._create_anomaly_alert(user_email, behavior_type, anomaly_score)

    def monitor_bulk_operations(
        self,
        user_id: int,
        user_email: str,
        operation_type: str,
        affected_records: int,
        operation_details: Dict[str, Any],
        ip_address: Optional[str] = None,
    ):
        """Monitor bulk operations that could indicate malicious activity."""
        # Log bulk operation
        self.audit_service.log_user_action(
            user_id=user_id,
            user_email=user_email,
            user_role=None,
            action=AuditAction.UPDATE,
            module="system",
            description=f"Bulk operation: {operation_type} affecting {affected_records} records",
            ip_address=ip_address,
            success=True,
            additional_data={
                "bulk_operation": True,
                "operation_type": operation_type,
                "affected_records": affected_records,
                "operation_details": operation_details,
            },
        )

        # Create alert for large bulk operations
        if affected_records > 100:  # Configurable threshold
            self._create_bulk_operation_alert(
                user_email, operation_type, affected_records
            )

    def check_data_integrity(
        self, table_name: str, expected_hash: str, actual_hash: str, record_count: int
    ):
        """Check data integrity and detect potential tampering."""
        integrity_valid = expected_hash == actual_hash

        # Log integrity check
        self.audit_service.log_security_event(
            event_type="data_integrity_check",
            description=f"Data integrity check for {table_name}: {'PASSED' if integrity_valid else 'FAILED'}",
            severity=AuditLevel.CRITICAL if not integrity_valid else AuditLevel.INFO,
            additional_data={
                "table_name": table_name,
                "expected_hash": expected_hash,
                "actual_hash": actual_hash,
                "record_count": record_count,
                "integrity_valid": integrity_valid,
            },
        )

        # Create critical alert for integrity failures
        if not integrity_valid:
            self._create_integrity_failure_alert(table_name, record_count)

        return integrity_valid

    # ============================================================================
    # PRIVATE HELPER METHODS
    # ============================================================================

    def _check_failed_login_patterns(self, user_email: str, ip_address: str):
        """Check for suspicious failed login patterns."""
        # Check failed logins in the last hour
        recent_time = datetime.utcnow() - timedelta(hours=1)

        from ..schemas import AuditLogFilter

        filters = AuditLogFilter(
            user_email=user_email,
            action=AuditAction.LOGIN,
            success=False,
            start_date=recent_time,
            limit=100,
        )

        failed_logins = self.audit_service.get_audit_logs(filters)

        # Alert if more than 5 failed logins in an hour
        if len(failed_logins) >= 5:
            self._create_brute_force_alert(user_email, ip_address, len(failed_logins))

        # Check for logins from multiple IPs
        unique_ips = set(log.ip_address for log in failed_logins if log.ip_address)
        if len(unique_ips) > 3:
            self._create_distributed_attack_alert(user_email, len(unique_ips))

    def _check_unauthorized_access_patterns(
        self,
        user_id: int,
        user_email: str,
        resource_type: str,
        ip_address: Optional[str],
    ):
        """Check for patterns of unauthorized access attempts."""
        recent_time = datetime.utcnow() - timedelta(hours=1)

        filters = AuditLogFilter(
            user_id=user_id,
            action=AuditAction.ACCESS_DENIED,
            resource_type=resource_type,
            start_date=recent_time,
            limit=50,
        )

        denied_attempts = self.audit_service.get_audit_logs(filters)

        # Alert if more than 10 denied attempts in an hour
        if len(denied_attempts) >= 10:
            self._create_unauthorized_access_alert(
                user_email, resource_type, len(denied_attempts)
            )

    def _check_sensitive_data_access_patterns(
        self, user_id: int, data_type: str, data_sensitivity: str
    ):
        """Check for unusual patterns in sensitive data access."""
        # Check access volume in the last 24 hours
        recent_time = datetime.utcnow() - timedelta(hours=24)

        filters = AuditLogFilter(
            user_id=user_id, resource_type=data_type, start_date=recent_time, limit=200
        )

        access_logs = self.audit_service.get_audit_logs(filters)

        # Alert for excessive access to sensitive data
        threshold = 50 if data_sensitivity == "restricted" else 100
        if len(access_logs) > threshold:
            self._create_excessive_data_access_alert(
                user_id, data_type, len(access_logs)
            )

    def _create_brute_force_alert(
        self, user_email: str, ip_address: str, attempt_count: int
    ):
        """Create alert for brute force login attempts."""
        from ..schemas import AlertCreate

        alert_data = AlertCreate(
            alert_type=AlertType.MULTIPLE_LOGIN_FAILURES,
            severity=AlertSeverity.HIGH,
            category=AlertCategory.SECURITY,
            title=f"Brute force attack detected on {user_email}",
            description=f"Multiple failed login attempts ({attempt_count}) detected for user {user_email} from IP {ip_address}",
            recommendation="Consider temporarily blocking the IP address and notifying the user",
            source_module="security",
            source_component="login_monitor",
            alert_data={
                "user_email": user_email,
                "ip_address": ip_address,
                "attempt_count": attempt_count,
                "attack_type": "brute_force",
            },
        )

        return self.alert_service.create_alert(alert_data)

    def _create_distributed_attack_alert(self, user_email: str, ip_count: int):
        """Create alert for distributed login attacks."""

        alert_data = AlertCreate(
            alert_type=AlertType.SUSPICIOUS_ACTIVITY,
            severity=AlertSeverity.CRITICAL,
            category=AlertCategory.SECURITY,
            title=f"Distributed attack detected on {user_email}",
            description=f"Failed login attempts from {ip_count} different IP addresses for user {user_email}",
            recommendation="Immediately lock the user account and investigate the attack pattern",
            source_module="security",
            source_component="login_monitor",
            alert_data={
                "user_email": user_email,
                "ip_count": ip_count,
                "attack_type": "distributed",
            },
        )

        return self.alert_service.create_alert(alert_data)

    def _create_unauthorized_access_alert(
        self, user_email: str, resource_type: str, attempt_count: int
    ):
        """Create alert for repeated unauthorized access attempts."""

        alert_data = AlertCreate(
            alert_type=AlertType.UNAUTHORIZED_ACCESS_ATTEMPT,
            severity=AlertSeverity.HIGH,
            category=AlertCategory.SECURITY,
            title=f"Repeated unauthorized access attempts by {user_email}",
            description=f"User {user_email} has made {attempt_count} unauthorized access attempts to {resource_type}",
            recommendation="Review user permissions and investigate potential privilege escalation attempt",
            source_module="security",
            source_component="access_monitor",
            alert_data={
                "user_email": user_email,
                "resource_type": resource_type,
                "attempt_count": attempt_count,
            },
        )

        return self.alert_service.create_alert(alert_data)

    def _create_privilege_escalation_alert(
        self, user_email: str, old_role: str, new_role: str, changed_by: int
    ):
        """Create alert for privilege escalation."""

        alert_data = AlertCreate(
            alert_type=AlertType.SUSPICIOUS_ACTIVITY,
            severity=AlertSeverity.HIGH,
            category=AlertCategory.SECURITY,
            title=f"Privilege escalation for {user_email}",
            description=f"User {user_email} privileges changed from {old_role} to {new_role}",
            recommendation="Verify the legitimacy of this privilege change",
            source_module="security",
            source_component="privilege_monitor",
            alert_data={
                "user_email": user_email,
                "old_role": old_role,
                "new_role": new_role,
                "changed_by_user_id": changed_by,
            },
        )

        return self.alert_service.create_alert(alert_data)

    def _create_configuration_change_alert(self, config_type: str, user_email: str):
        """Create alert for critical configuration changes."""

        alert_data = AlertCreate(
            alert_type=AlertType.SUSPICIOUS_ACTIVITY,
            severity=AlertSeverity.MEDIUM,
            category=AlertCategory.SECURITY,
            title=f"Critical configuration change: {config_type}",
            description=f"Critical system configuration {config_type} was modified by {user_email}",
            recommendation="Review the configuration change and ensure it was authorized",
            source_module="security",
            source_component="config_monitor",
            alert_data={"configuration_type": config_type, "changed_by": user_email},
        )

        return self.alert_service.create_alert(alert_data)

    def _create_anomaly_alert(
        self, user_email: str, behavior_type: str, anomaly_score: float
    ):
        """Create alert for anomalous behavior."""

        alert_data = AlertCreate(
            alert_type=AlertType.ANOMALOUS_USER_BEHAVIOR,
            severity=AlertSeverity.HIGH,
            category=AlertCategory.SECURITY,
            title=f"Anomalous behavior detected: {user_email}",
            description=f"User {user_email} exhibited anomalous {behavior_type} behavior (score: {anomaly_score:.2f})",
            recommendation="Investigate user activity and consider temporary access restrictions",
            source_module="security",
            source_component="anomaly_detector",
            alert_data={
                "user_email": user_email,
                "behavior_type": behavior_type,
                "anomaly_score": anomaly_score,
            },
        )

        return self.alert_service.create_alert(alert_data)

    def _create_bulk_operation_alert(
        self, user_email: str, operation_type: str, affected_records: int
    ):
        """Create alert for large bulk operations."""

        alert_data = AlertCreate(
            alert_type=AlertType.SUSPICIOUS_ACTIVITY,
            severity=AlertSeverity.MEDIUM,
            category=AlertCategory.SECURITY,
            title=f"Large bulk operation by {user_email}",
            description=f"User {user_email} performed {operation_type} affecting {affected_records} records",
            recommendation="Verify the legitimacy of this bulk operation",
            source_module="security",
            source_component="bulk_monitor",
            alert_data={
                "user_email": user_email,
                "operation_type": operation_type,
                "affected_records": affected_records,
            },
        )

        return self.alert_service.create_alert(alert_data)

    def _create_excessive_data_access_alert(
        self, user_id: int, data_type: str, access_count: int
    ):
        """Create alert for excessive sensitive data access."""

        alert_data = AlertCreate(
            alert_type=AlertType.SUSPICIOUS_ACTIVITY,
            severity=AlertSeverity.MEDIUM,
            category=AlertCategory.SECURITY,
            title=f"Excessive sensitive data access",
            description=f"User ID {user_id} accessed {data_type} data {access_count} times in 24 hours",
            recommendation="Review user's data access patterns and verify business justification",
            source_module="security",
            source_component="data_access_monitor",
            alert_data={
                "user_id": user_id,
                "data_type": data_type,
                "access_count": access_count,
            },
        )

        return self.alert_service.create_alert(alert_data)

    def _create_integrity_failure_alert(self, table_name: str, record_count: int):
        """Create critical alert for data integrity failures."""

        alert_data = AlertCreate(
            alert_type=AlertType.SECURITY_BREACH,
            severity=AlertSeverity.CRITICAL,
            category=AlertCategory.SECURITY,
            title=f"Data integrity failure: {table_name}",
            description=f"Data integrity check failed for table {table_name} with {record_count} records",
            recommendation="Immediately investigate potential data tampering and restore from backup if necessary",
            source_module="security",
            source_component="integrity_monitor",
            alert_data={
                "table_name": table_name,
                "record_count": record_count,
                "integrity_check": "failed",
            },
        )

        return self.alert_service.create_alert(alert_data)

    def _operation_to_audit_action(self, operation: str) -> AuditAction:
        """Convert operation string to audit action."""
        operation_lower = operation.lower()

        if operation_lower == "create":
            return AuditAction.CREATE
        elif operation_lower == "update":
            return AuditAction.UPDATE
        elif operation_lower == "delete":
            return AuditAction.DELETE
        elif operation_lower == "read":
            return AuditAction.READ
        else:
            return AuditAction.READ

    def _is_critical_configuration(self, config_type: str) -> bool:
        """Determine if a configuration type is critical."""
        critical_configs = [
            "database_connection",
            "authentication_settings",
            "encryption_keys",
            "security_policies",
            "admin_permissions",
            "backup_settings",
            "logging_configuration",
        ]

        return config_type.lower() in critical_configs
