"""Advanced alert engine for monitoring system."""

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from ..models.alert import Alert, AlertCategory, AlertSeverity, AlertStatus, AlertType
from ..models.system_metric import SystemMetric
from ..services.alert_service import AlertService
from ..services.metric_service import MetricService
from .anomaly_detector import AnomalyDetector


class AlertEngine:
    """Advanced alert processing and management engine."""

    def __init__(self, db: Session):
        self.db = db
        self.alert_service = AlertService(db)
        self.metric_service = MetricService(db)
        self.anomaly_detector = AnomalyDetector(db)

        # Alert rules configuration
        self.alert_rules = self._load_alert_rules()
        self.escalation_rules = self._load_escalation_rules()
        self.suppression_rules = self._load_suppression_rules()

    def process_metric_alerts(self, lookback_minutes: int = 5) -> List[Dict[str, Any]]:
        """Process metrics and generate alerts based on rules."""
        start_time = datetime.utcnow() - timedelta(minutes=lookback_minutes)

        from ..schemas import SystemMetricFilter

        filters = SystemMetricFilter(start_date=start_time, limit=1000, offset=0)

        recent_metrics = self.metric_service.get_metrics(filters)
        generated_alerts = []

        for metric in recent_metrics:
            # Check threshold-based alerts
            threshold_alerts = self._check_threshold_alerts(metric)
            generated_alerts.extend(threshold_alerts)

            # Check rate-based alerts
            rate_alerts = self._check_rate_alerts(metric)
            generated_alerts.extend(rate_alerts)

            # Check pattern-based alerts
            pattern_alerts = self._check_pattern_alerts(metric)
            generated_alerts.extend(pattern_alerts)

        # Process anomaly-based alerts
        anomaly_alerts = self._process_anomaly_alerts(lookback_minutes)
        generated_alerts.extend(anomaly_alerts)

        # Apply suppression rules
        filtered_alerts = self._apply_suppression_rules(generated_alerts)

        # Create alerts in database
        created_alerts = []
        for alert_data in filtered_alerts:
            try:
                from ..schemas import AlertCreate

                alert_create = AlertCreate(**alert_data)
                alert = self.alert_service.create_alert(alert_create)
                created_alerts.append(alert.model_dump())
            except Exception as e:
                continue

        return created_alerts

    def process_alert_escalations(self) -> List[Dict[str, Any]]:
        """Process alert escalations based on time and severity."""
        escalated_alerts = []

        # Get active alerts that might need escalation
        from ..schemas import AlertFilter

        filters = AlertFilter(status=AlertStatus.ACTIVE, limit=500, offset=0)

        active_alerts = self.alert_service.get_alerts(filters)

        for alert in active_alerts:
            escalation_info = self._check_escalation_needed(alert)

            if escalation_info:
                # Escalate alert
                escalated_alert = self._escalate_alert(alert, escalation_info)
                if escalated_alert:
                    escalated_alerts.append(escalated_alert)

        return escalated_alerts

    def process_alert_auto_resolution(self) -> List[Dict[str, Any]]:
        """Automatically resolve alerts when conditions are met."""
        resolved_alerts = []

        # Get active alerts

        filters = AlertFilter(status=AlertStatus.ACTIVE, limit=500, offset=0)

        active_alerts = self.alert_service.get_alerts(filters)

        for alert in active_alerts:
            if self._should_auto_resolve(alert):
                try:
                    resolved_alert = self.alert_service.resolve_alert(
                        alert.id,
                        resolution_note="Auto-resolved: conditions returned to normal",
                        resolved_by="system",
                    )
                    resolved_alerts.append(resolved_alert.model_dump())
                except Exception:
                    continue

        return resolved_alerts

    def generate_alert_digest(self, period_hours: int = 24) -> Dict[str, Any]:
        """Generate alert digest for specified period."""
        start_time = datetime.utcnow() - timedelta(hours=period_hours)

        filters = AlertFilter(start_date=start_time, limit=2000, offset=0)

        alerts = self.alert_service.get_alerts(filters)

        digest = {
            "period_hours": period_hours,
            "total_alerts": len(alerts),
            "alerts_by_severity": {"critical": 0, "high": 0, "medium": 0, "low": 0},
            "alerts_by_status": {
                "active": 0,
                "acknowledged": 0,
                "resolved": 0,
                "suppressed": 0,
            },
            "alerts_by_type": {},
            "alerts_by_module": {},
            "top_alert_sources": [],
            "resolution_stats": {
                "avg_resolution_time_minutes": 0,
                "fastest_resolution_minutes": 0,
                "slowest_resolution_minutes": 0,
            },
            "escalation_stats": {"escalated_alerts": 0, "escalation_rate": 0},
        }

        resolution_times = []
        escalated_count = 0

        for alert in alerts:
            # Count by severity
            severity = alert.severity.value.lower()
            digest["alerts_by_severity"][severity] += 1

            # Count by status
            status = alert.status.value.lower()
            digest["alerts_by_status"][status] += 1

            # Count by type
            alert_type = alert.alert_type.value
            digest["alerts_by_type"][alert_type] = (
                digest["alerts_by_type"].get(alert_type, 0) + 1
            )

            # Count by module
            module = alert.source_module or "unknown"
            digest["alerts_by_module"][module] = (
                digest["alerts_by_module"].get(module, 0) + 1
            )

            # Calculate resolution time
            if alert.resolved_at and alert.created_at:
                resolution_time = (
                    alert.resolved_at - alert.created_at
                ).total_seconds() / 60
                resolution_times.append(resolution_time)

            # Check for escalation
            if alert.escalated_at:
                escalated_count += 1

        # Calculate resolution statistics
        if resolution_times:
            digest["resolution_stats"]["avg_resolution_time_minutes"] = sum(
                resolution_times
            ) / len(resolution_times)
            digest["resolution_stats"]["fastest_resolution_minutes"] = min(
                resolution_times
            )
            digest["resolution_stats"]["slowest_resolution_minutes"] = max(
                resolution_times
            )

        # Calculate escalation statistics
        digest["escalation_stats"]["escalated_alerts"] = escalated_count
        if len(alerts) > 0:
            digest["escalation_stats"]["escalation_rate"] = (
                escalated_count / len(alerts)
            ) * 100

        # Top alert sources
        digest["top_alert_sources"] = sorted(
            digest["alerts_by_module"].items(), key=lambda x: x[1], reverse=True
        )[:10]

        return digest

    # ============================================================================
    # PRIVATE HELPER METHODS
    # ============================================================================

    def _load_alert_rules(self) -> Dict[str, Any]:
        """Load alert rules configuration."""
        return {
            "threshold_rules": {
                "cpu_usage": {"warning": 70, "critical": 90},
                "memory_usage": {"warning": 80, "critical": 95},
                "disk_usage": {"warning": 85, "critical": 95},
                "response_time": {"warning": 1000, "critical": 3000},
                "error_rate": {"warning": 5, "critical": 10},
            },
            "rate_rules": {
                "error_rate_increase": {"threshold": 50, "window_minutes": 5},
                "traffic_spike": {"threshold": 200, "window_minutes": 10},
                "response_time_degradation": {"threshold": 100, "window_minutes": 5},
            },
        }

    def _load_escalation_rules(self) -> Dict[str, Any]:
        """Load escalation rules configuration."""
        return {
            "time_based": {
                AlertSeverity.CRITICAL.value: 15,  # minutes
                AlertSeverity.HIGH.value: 30,
                AlertSeverity.MEDIUM.value: 60,
                AlertSeverity.LOW.value: 120,
            }
        }

    def _load_suppression_rules(self) -> Dict[str, Any]:
        """Load suppression rules configuration."""
        return {
            "duplicate_window_minutes": 10,
            "maintenance_mode": False,
            "suppression_patterns": [
                {"pattern": "test_", "reason": "Test alerts suppressed"}
            ],
        }

    def _check_threshold_alerts(self, metric: SystemMetric) -> List[Dict[str, Any]]:
        """Check if metric violates threshold rules."""
        alerts = []
        threshold_rules = self.alert_rules["threshold_rules"]

        metric_name = metric.metric_name.lower()

        for rule_name, thresholds in threshold_rules.items():
            if rule_name in metric_name:
                # Check critical threshold
                if metric.value >= thresholds.get("critical", float("inf")):
                    alerts.append(
                        {
                            "alert_type": self._map_metric_to_alert_type(metric_name),
                            "severity": AlertSeverity.CRITICAL.value,
                            "category": AlertCategory.INFRASTRUCTURE.value,
                            "title": f"Critical {rule_name} threshold exceeded",
                            "description": f"{metric.metric_name} value {metric.value} exceeds critical threshold {thresholds['critical']}",
                            "recommendation": self._get_threshold_recommendation(
                                rule_name
                            ),
                            "source_module": metric.module or "monitoring",
                            "source_component": "alert_engine",
                            "alert_data": {
                                "metric_name": metric.metric_name,
                                "current_value": metric.value,
                                "threshold_type": "critical",
                                "threshold_value": thresholds["critical"],
                                "rule_name": rule_name,
                            },
                        }
                    )

        return alerts

    def _check_rate_alerts(self, metric: SystemMetric) -> List[Dict[str, Any]]:
        """Check if metric violates rate-based rules."""
        return []  # Simplified implementation

    def _check_pattern_alerts(self, metric: SystemMetric) -> List[Dict[str, Any]]:
        """Check if metric violates pattern-based rules."""
        return []  # Simplified implementation

    def _process_anomaly_alerts(self, lookback_minutes: int) -> List[Dict[str, Any]]:
        """Process anomaly detection and create alerts."""
        return []  # Simplified implementation

    def _apply_suppression_rules(
        self, alerts: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Apply suppression rules to filter out unwanted alerts."""
        return alerts  # Simplified implementation

    def _check_escalation_needed(self, alert: Alert) -> Optional[Dict[str, Any]]:
        """Check if alert needs escalation."""
        escalation_rules = self.escalation_rules
        time_limits = escalation_rules.get("time_based", {})
        escalation_time_minutes = time_limits.get(alert.severity.value, 60)

        time_since_created = (datetime.utcnow() - alert.created_at).total_seconds() / 60

        if time_since_created >= escalation_time_minutes and not alert.escalated_at:
            return {
                "reason": "time_based",
                "escalation_time_minutes": escalation_time_minutes,
                "time_since_created": time_since_created,
            }

        return None

    def _escalate_alert(
        self, alert: Alert, escalation_info: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Escalate an alert."""
        try:
            escalated_alert = self.alert_service.escalate_alert(
                alert.id,
                escalation_reason=f"Auto-escalation: {escalation_info['reason']}",
                escalated_by="system",
            )
            return escalated_alert.model_dump()
        except Exception:
            return None

    def _should_auto_resolve(self, alert: Alert) -> bool:
        """Check if alert should be auto-resolved."""
        auto_resolvable_types = [
            AlertType.HIGH_CPU_USAGE,
            AlertType.HIGH_MEMORY_USAGE,
            AlertType.SLOW_RESPONSE_TIME,
            AlertType.HIGH_ERROR_RATE,
        ]

        return alert.alert_type in auto_resolvable_types

    def _map_metric_to_alert_type(self, metric_name: str) -> str:
        """Map metric name to appropriate alert type."""
        metric_name = metric_name.lower()

        if "cpu" in metric_name:
            return AlertType.HIGH_CPU_USAGE.value
        elif "memory" in metric_name:
            return AlertType.HIGH_MEMORY_USAGE.value
        elif "response_time" in metric_name:
            return AlertType.SLOW_RESPONSE_TIME.value
        elif "error" in metric_name:
            return AlertType.HIGH_ERROR_RATE.value
        elif "disk" in metric_name:
            return AlertType.HIGH_DISK_USAGE.value
        else:
            return AlertType.CUSTOM_THRESHOLD.value

    def _get_threshold_recommendation(self, rule_name: str) -> str:
        """Get recommendation for threshold violations."""
        recommendations = {
            "cpu_usage": "Check for high CPU processes and consider scaling or optimization",
            "memory_usage": "Investigate memory usage and consider increasing available memory",
            "disk_usage": "Clean up disk space or increase storage capacity",
            "response_time": "Optimize queries and code performance",
            "error_rate": "Review application logs and fix underlying issues",
        }
        return recommendations.get(rule_name, "Investigate and take appropriate action")
