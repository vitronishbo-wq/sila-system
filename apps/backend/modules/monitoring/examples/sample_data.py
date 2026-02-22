"""Sample data generator for monitoring module testing."""

import random
import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from ..models.alert import Alert, AlertCategory, AlertSeverity, AlertStatus, AlertType
from ..models.audit_log import AuditLog
from ..models.system_metric import MetricCategory, MetricType, MetricUnit, SystemMetric


class SampleDataGenerator:
    """Generate sample data for monitoring module testing."""

    def __init__(self, db: Session):
        self.db = db

        # Sample data configurations
        self.modules = [
            "citizenship",
            "health",
            "finance",
            "justice",
            "governance",
            "complaints",
        ]
        self.actions = [
            "CREATE",
            "READ",
            "UPDATE",
            "DELETE",
            "LOGIN",
            "LOGOUT",
            "EXPORT",
            "IMPORT",
        ]
        self.metric_names = [
            "cpu_usage_percent",
            "memory_usage_percent",
            "disk_usage_percent",
            "response_time_ms",
            "request_count",
            "error_count",
            "active_users",
            "database_connections",
            "network_throughput_mbps",
            "queue_size",
        ]
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
        ]
        self.ip_addresses = [
            "192.168.1.100",
            "192.168.1.101",
            "10.0.0.50",
            "172.16.0.10",
            "203.0.113.1",
            "198.51.100.1",
            "192.0.2.1",
        ]

    def generate_audit_logs(
        self, count: int = 100, days_back: int = 7
    ) -> List[AuditLog]:
        """Generate sample audit logs."""
        audit_logs = []

        for i in range(count):
            # Random timestamp within the last N days
            random_time = datetime.utcnow() - timedelta(
                days=random.randint(0, days_back),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59),
            )

            # Create audit log
            audit_log = AuditLog(
                user_id=random.randint(1, 50),
                user_email=f"user{random.randint(1, 50)}@sila.gov.ao",
                action=random.choice(self.actions),
                module=random.choice(self.modules),
                resource_type=f"{random.choice(self.modules)}_resource",
                resource_id=str(random.randint(1, 1000)),
                description=self._generate_audit_description(),
                ip_address=random.choice(self.ip_addresses),
                user_agent=random.choice(self.user_agents),
                session_id=str(uuid.uuid4()),
                timestamp=random_time,
                metadata=self._generate_audit_metadata(),
                hash_value=f"hash_{uuid.uuid4().hex[:16]}",
                previous_hash=f"prev_hash_{uuid.uuid4().hex[:16]}" if i > 0 else None,
            )

            audit_logs.append(audit_log)

        return audit_logs

    def generate_system_metrics(
        self, count: int = 200, days_back: int = 7
    ) -> List[SystemMetric]:
        """Generate sample system metrics."""
        metrics = []

        for i in range(count):
            # Random timestamp within the last N days
            random_time = datetime.utcnow() - timedelta(
                days=random.randint(0, days_back),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59),
            )

            metric_name = random.choice(self.metric_names)

            # Generate realistic values based on metric type
            value = self._generate_metric_value(metric_name)

            metric = SystemMetric(
                metric_name=metric_name,
                metric_type=self._get_metric_type(metric_name),
                value=value,
                unit=self._get_metric_unit(metric_name),
                category=self._get_metric_category(metric_name),
                module=random.choice(self.modules),
                component=f"{random.choice(self.modules)}_service",
                tags=self._generate_metric_tags(),
                metadata=self._generate_metric_metadata(),
                timestamp=random_time,
                warning_threshold=self._get_warning_threshold(metric_name),
                critical_threshold=self._get_critical_threshold(metric_name),
                is_anomaly=secrets.randbelow() < 0.05,  # 5% chance of anomaly
            )

            metrics.append(metric)

        return metrics

    def generate_alerts(self, count: int = 50, days_back: int = 7) -> List[Alert]:
        """Generate sample alerts."""
        alerts = []

        alert_types = list(AlertType)
        severities = list(AlertSeverity)
        statuses = list(AlertStatus)
        categories = list(AlertCategory)

        for i in range(count):
            # Random timestamp within the last N days
            random_time = datetime.utcnow() - timedelta(
                days=random.randint(0, days_back),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59),
            )

            alert_type = random.choice(alert_types)
            severity = random.choice(severities)
            status = random.choice(statuses)

            alert = Alert(
                alert_type=alert_type,
                severity=severity,
                status=status,
                category=random.choice(categories),
                title=self._generate_alert_title(alert_type),
                description=self._generate_alert_description(alert_type),
                recommendation=self._generate_alert_recommendation(alert_type),
                source_module=random.choice(self.modules),
                source_component=f"{random.choice(self.modules)}_service",
                alert_data=self._generate_alert_data(alert_type),
                tags=self._generate_alert_tags(),
                created_at=random_time,
                acknowledged_at=(
                    random_time + timedelta(minutes=random.randint(5, 60))
                    if status != AlertStatus.ACTIVE
                    else None
                ),
                acknowledged_by=(
                    f"user{random.randint(1, 10)}"
                    if status != AlertStatus.ACTIVE
                    else None
                ),
                resolved_at=(
                    random_time + timedelta(hours=random.randint(1, 24))
                    if status == AlertStatus.RESOLVED
                    else None
                ),
                resolved_by=(
                    f"user{random.randint(1, 10)}"
                    if status == AlertStatus.RESOLVED
                    else None
                ),
                escalated_at=(
                    random_time + timedelta(hours=random.randint(2, 12))
                    if secrets.randbelow() < 0.2
                    else None
                ),
                escalated_by="system" if secrets.randbelow() < 0.2 else None,
                suppressed_at=(
                    random_time + timedelta(minutes=random.randint(10, 120))
                    if status == AlertStatus.SUPPRESSED
                    else None
                ),
                suppressed_by=(
                    f"user{random.randint(1, 10)}"
                    if status == AlertStatus.SUPPRESSED
                    else None
                ),
            )

            alerts.append(alert)

        return alerts

    def create_realistic_scenario(
        self, scenario_name: str = "normal_operations"
    ) -> Dict[str, List]:
        """Create a realistic monitoring scenario with correlated data."""
        scenarios = {
            "normal_operations": self._create_normal_operations_scenario(),
            "high_load": self._create_high_load_scenario(),
            "system_issues": self._create_system_issues_scenario(),
            "security_incident": self._create_security_incident_scenario(),
            "maintenance_window": self._create_maintenance_window_scenario(),
        }

        return scenarios.get(scenario_name, scenarios["normal_operations"])

    def populate_database(
        self, scenario: str = "normal_operations", scale: str = "small"
    ):
        """Populate database with sample data."""
        scale_multipliers = {"small": 1, "medium": 3, "large": 10}

        multiplier = scale_multipliers.get(scale, 1)

        # Generate and save data
        scenario_data = self.create_realistic_scenario(scenario)

        # Save audit logs
        for audit_log in scenario_data["audit_logs"][: 100 * multiplier]:
            self.db.add(audit_log)

        # Save metrics
        for metric in scenario_data["metrics"][: 200 * multiplier]:
            self.db.add(metric)

        # Save alerts
        for alert in scenario_data["alerts"][: 50 * multiplier]:
            self.db.add(alert)

        try:
            self.db.commit()
            return {
                "status": "success",
                "audit_logs_created": len(
                    scenario_data["audit_logs"][: 100 * multiplier]
                ),
                "metrics_created": len(scenario_data["metrics"][: 200 * multiplier]),
                "alerts_created": len(scenario_data["alerts"][: 50 * multiplier]),
            }
        except Exception as e:
            self.db.rollback()
            return {"status": "error", "message": str(e)}

    # ============================================================================
    # PRIVATE HELPER METHODS
    # ============================================================================

    def _generate_audit_description(self) -> str:
        """Generate realistic audit log description."""
        descriptions = [
            "User successfully logged into the system",
            "Created new citizen record with validation",
            "Updated user profile information",
            "Deleted expired document record",
            "Exported citizen data for reporting",
            "Failed login attempt - invalid credentials",
            "Password reset requested",
            "Document uploaded and processed",
            "System backup completed successfully",
            "Database maintenance performed",
        ]
        return random.choice(descriptions)

    def _generate_audit_metadata(self) -> Dict[str, Any]:
        """Generate audit log metadata."""
        return {
            "browser": random.choice(["Chrome", "Firefox", "Safari", "Edge"]),
            "os": random.choice(["Windows", "macOS", "Linux"]),
            "request_id": str(uuid.uuid4()),
            "duration_ms": random.randint(50, 2000),
            "status_code": random.choice([200, 201, 400, 401, 403, 404, 500]),
        }

    def _generate_metric_value(self, metric_name: str) -> float:
        """Generate realistic metric values based on metric type."""
        if "cpu_usage" in metric_name or "memory_usage" in metric_name:
            return round(random.uniform(10, 95), 2)
        elif "disk_usage" in metric_name:
            return round(random.uniform(20, 90), 2)
        elif "response_time" in metric_name:
            return round(random.uniform(50, 3000), 2)
        elif "count" in metric_name:
            return random.randint(0, 1000)
        elif "throughput" in metric_name:
            return round(random.uniform(1, 100), 2)
        else:
            return round(random.uniform(0, 100), 2)

    def _get_metric_type(self, metric_name: str) -> MetricType:
        """Get metric type based on metric name."""
        if "count" in metric_name:
            return MetricType.COUNTER
        elif "usage" in metric_name or "percent" in metric_name:
            return MetricType.GAUGE
        elif "time" in metric_name:
            return MetricType.HISTOGRAM
        else:
            return MetricType.GAUGE

    def _get_metric_unit(self, metric_name: str) -> MetricUnit:
        """Get metric unit based on metric name."""
        if "percent" in metric_name:
            return MetricUnit.PERCENT
        elif "ms" in metric_name:
            return MetricUnit.MILLISECONDS
        elif "mbps" in metric_name:
            return MetricUnit.MEGABYTES_PER_SECOND
        elif "count" in metric_name:
            return MetricUnit.COUNT
        else:
            return MetricUnit.NONE

    def _get_metric_category(self, metric_name: str) -> MetricCategory:
        """Get metric category based on metric name."""
        if any(word in metric_name for word in ["cpu", "memory", "disk"]):
            return MetricCategory.SYSTEM
        elif any(word in metric_name for word in ["response", "request", "throughput"]):
            return MetricCategory.PERFORMANCE
        elif "error" in metric_name:
            return MetricCategory.ERROR
        elif "user" in metric_name:
            return MetricCategory.BUSINESS
        else:
            return MetricCategory.APPLICATION

    def _generate_metric_tags(self) -> Dict[str, str]:
        """Generate metric tags."""
        return {
            "environment": random.choice(["production", "staging", "development"]),
            "region": random.choice(["luanda", "benguela", "huambo"]),
            "service": random.choice(["api", "web", "worker", "database"]),
        }

    def _generate_metric_metadata(self) -> Dict[str, Any]:
        """Generate metric metadata."""
        return {
            "collection_method": random.choice(["agent", "api", "log_parsing"]),
            "source_host": f"server-{random.randint(1, 10)}",
            "collection_interval": random.choice([30, 60, 300]),
        }

    def _get_warning_threshold(self, metric_name: str) -> Optional[float]:
        """Get warning threshold for metric."""
        thresholds = {
            "cpu_usage_percent": 70.0,
            "memory_usage_percent": 80.0,
            "disk_usage_percent": 85.0,
            "response_time_ms": 1000.0,
            "error_count": 10.0,
        }
        return thresholds.get(metric_name)

    def _get_critical_threshold(self, metric_name: str) -> Optional[float]:
        """Get critical threshold for metric."""
        thresholds = {
            "cpu_usage_percent": 90.0,
            "memory_usage_percent": 95.0,
            "disk_usage_percent": 95.0,
            "response_time_ms": 3000.0,
            "error_count": 50.0,
        }
        return thresholds.get(metric_name)

    def _generate_alert_title(self, alert_type: AlertType) -> str:
        """Generate alert title based on type."""
        titles = {
            AlertType.HIGH_CPU_USAGE: "High CPU Usage Detected",
            AlertType.HIGH_MEMORY_USAGE: "Memory Usage Critical",
            AlertType.HIGH_DISK_USAGE: "Disk Space Running Low",
            AlertType.SLOW_RESPONSE_TIME: "Application Response Time Degraded",
            AlertType.HIGH_ERROR_RATE: "Error Rate Spike Detected",
            AlertType.SERVICE_UNAVAILABLE: "Service Unavailable",
            AlertType.DATABASE_CONNECTION_FAILED: "Database Connection Issues",
            AlertType.UNUSUAL_TRAFFIC_PATTERN: "Unusual Traffic Pattern Detected",
            AlertType.SECURITY_BREACH_ATTEMPT: "Security Breach Attempt",
            AlertType.ANOMALY_DETECTED: "System Anomaly Detected",
        }
        return titles.get(alert_type, "System Alert")

    def _generate_alert_description(self, alert_type: AlertType) -> str:
        """Generate alert description based on type."""
        descriptions = {
            AlertType.HIGH_CPU_USAGE: "CPU usage has exceeded the warning threshold and requires attention",
            AlertType.HIGH_MEMORY_USAGE: "Memory usage is critically high and may impact system performance",
            AlertType.HIGH_DISK_USAGE: "Disk usage is approaching capacity limits",
            AlertType.SLOW_RESPONSE_TIME: "Application response times are significantly higher than normal",
            AlertType.HIGH_ERROR_RATE: "Error rate has spiked above acceptable levels",
            AlertType.SERVICE_UNAVAILABLE: "Critical service is not responding to health checks",
            AlertType.DATABASE_CONNECTION_FAILED: "Unable to establish connection to database",
            AlertType.UNUSUAL_TRAFFIC_PATTERN: "Traffic pattern deviates significantly from normal baseline",
            AlertType.SECURITY_BREACH_ATTEMPT: "Potential security breach attempt detected",
            AlertType.ANOMALY_DETECTED: "System behavior anomaly detected by monitoring algorithms",
        }
        return descriptions.get(alert_type, "System alert requiring attention")

    def _generate_alert_recommendation(self, alert_type: AlertType) -> str:
        """Generate alert recommendation based on type."""
        recommendations = {
            AlertType.HIGH_CPU_USAGE: "Check for high CPU processes and consider scaling or optimization",
            AlertType.HIGH_MEMORY_USAGE: "Investigate memory leaks and consider increasing available memory",
            AlertType.HIGH_DISK_USAGE: "Clean up disk space or increase storage capacity",
            AlertType.SLOW_RESPONSE_TIME: "Optimize database queries and application performance",
            AlertType.HIGH_ERROR_RATE: "Review application logs and fix underlying issues",
            AlertType.SERVICE_UNAVAILABLE: "Restart service and investigate root cause",
            AlertType.DATABASE_CONNECTION_FAILED: "Check database connectivity and configuration",
            AlertType.UNUSUAL_TRAFFIC_PATTERN: "Investigate traffic source and potential DDoS attack",
            AlertType.SECURITY_BREACH_ATTEMPT: "Review security logs and strengthen access controls",
            AlertType.ANOMALY_DETECTED: "Investigate anomaly cause and take corrective action",
        }
        return recommendations.get(
            alert_type, "Investigate and take appropriate action"
        )

    def _generate_alert_data(self, alert_type: AlertType) -> Dict[str, Any]:
        """Generate alert-specific data."""
        return {
            "threshold_value": random.uniform(70, 95),
            "current_value": random.uniform(80, 100),
            "duration_minutes": random.randint(5, 120),
            "affected_components": [random.choice(self.modules)],
            "correlation_id": str(uuid.uuid4()),
        }

    def _generate_alert_tags(self) -> Dict[str, str]:
        """Generate alert tags."""
        return {
            "priority": random.choice(["high", "medium", "low"]),
            "team": random.choice(["infrastructure", "application", "security"]),
            "environment": random.choice(["production", "staging"]),
        }

    def _create_normal_operations_scenario(self) -> Dict[str, List]:
        """Create normal operations scenario."""
        return {
            "audit_logs": self.generate_audit_logs(100, 7),
            "metrics": self.generate_system_metrics(200, 7),
            "alerts": self.generate_alerts(20, 7),  # Fewer alerts in normal operations
        }

    def _create_high_load_scenario(self) -> Dict[str, List]:
        """Create high load scenario with elevated metrics."""
        # Generate metrics with higher values
        metrics = []
        for i in range(300):  # More metrics during high load
            random_time = datetime.utcnow() - timedelta(
                hours=random.randint(0, 24), minutes=random.randint(0, 59)
            )

            metric_name = random.choice(self.metric_names)
            # Increase values for high load scenario
            base_value = self._generate_metric_value(metric_name)
            if "usage" in metric_name:
                value = min(100, base_value * 1.3)  # 30% higher usage
            elif "response_time" in metric_name:
                value = base_value * 2  # Double response time
            elif "count" in metric_name:
                value = base_value * 3  # Triple request count
            else:
                value = base_value * 1.2

            metric = SystemMetric(
                metric_name=metric_name,
                metric_type=self._get_metric_type(metric_name),
                value=value,
                unit=self._get_metric_unit(metric_name),
                category=self._get_metric_category(metric_name),
                module=random.choice(self.modules),
                component=f"{random.choice(self.modules)}_service",
                tags=self._generate_metric_tags(),
                metadata=self._generate_metric_metadata(),
                timestamp=random_time,
                warning_threshold=self._get_warning_threshold(metric_name),
                critical_threshold=self._get_critical_threshold(metric_name),
                is_anomaly=secrets.randbelow() < 0.15,  # Higher anomaly rate
            )

            metrics.append(metric)

        return {
            "audit_logs": self.generate_audit_logs(200, 3),  # More activity
            "metrics": metrics,
            "alerts": self.generate_alerts(80, 3),  # More alerts
        }

    def _create_system_issues_scenario(self) -> Dict[str, List]:
        """Create system issues scenario with errors and alerts."""
        # Generate error-heavy audit logs
        error_logs = []
        for i in range(50):
            random_time = datetime.utcnow() - timedelta(
                hours=random.randint(0, 12), minutes=random.randint(0, 59)
            )

            audit_log = AuditLog(
                user_id=random.randint(1, 50),
                user_email=f"user{random.randint(1, 50)}@sila.gov.ao",
                action="ERROR",
                module=random.choice(self.modules),
                resource_type="system",
                resource_id="error",
                description=random.choice(
                    [
                        "Database connection timeout",
                        "Service unavailable error",
                        "Authentication service failure",
                        "File system error",
                        "Network connectivity issue",
                    ]
                ),
                ip_address=random.choice(self.ip_addresses),
                user_agent=random.choice(self.user_agents),
                session_id=str(uuid.uuid4()),
                timestamp=random_time,
                metadata={"error_code": random.choice([500, 503, 504, 502])},
                hash_value=f"hash_{uuid.uuid4().hex[:16]}",
                previous_hash=f"prev_hash_{uuid.uuid4().hex[:16]}" if i > 0 else None,
            )

            error_logs.append(audit_log)

        # Add normal logs
        normal_logs = self.generate_audit_logs(100, 2)
        all_logs = error_logs + normal_logs

        return {
            "audit_logs": all_logs,
            "metrics": self.generate_system_metrics(250, 2),
            "alerts": self.generate_alerts(100, 2),  # Many alerts during issues
        }

    def _create_security_incident_scenario(self) -> Dict[str, List]:
        """Create security incident scenario."""
        # Generate security-related audit logs
        security_logs = []
        suspicious_ips = ["203.0.113.100", "198.51.100.200", "192.0.2.300"]

        for i in range(30):
            random_time = datetime.utcnow() - timedelta(
                hours=random.randint(0, 6), minutes=random.randint(0, 59)
            )

            audit_log = AuditLog(
                user_id=None,  # No user for failed attempts
                user_email=None,
                action=random.choice(
                    ["LOGIN_FAILED", "ACCESS_DENIED", "SUSPICIOUS_ACTIVITY"]
                ),
                module="security",
                resource_type="authentication",
                resource_id="security_event",
                description=random.choice(
                    [
                        "Multiple failed login attempts",
                        "Access denied - insufficient privileges",
                        "Suspicious file access pattern",
                        "Potential brute force attack",
                        "Unauthorized API access attempt",
                    ]
                ),
                ip_address=random.choice(suspicious_ips),
                user_agent="Suspicious User Agent",
                session_id=str(uuid.uuid4()),
                timestamp=random_time,
                metadata={"threat_level": "high", "blocked": True},
                hash_value=f"hash_{uuid.uuid4().hex[:16]}",
                previous_hash=f"prev_hash_{uuid.uuid4().hex[:16]}" if i > 0 else None,
            )

            security_logs.append(audit_log)

        # Add normal logs
        normal_logs = self.generate_audit_logs(70, 1)
        all_logs = security_logs + normal_logs

        return {
            "audit_logs": all_logs,
            "metrics": self.generate_system_metrics(150, 1),
            "alerts": self.generate_alerts(60, 1),  # Security alerts
        }

    def _create_maintenance_window_scenario(self) -> Dict[str, List]:
        """Create maintenance window scenario with reduced activity."""
        return {
            "audit_logs": self.generate_audit_logs(30, 1),  # Reduced activity
            "metrics": self.generate_system_metrics(100, 1),  # Fewer metrics
            "alerts": self.generate_alerts(5, 1),  # Minimal alerts
        }
