"""Alert service for the monitoring module."""

from datetime import datetime, timedelta
from typing import List, Optional

from sqlalchemy import and_, desc, or_
from sqlalchemy.orm import Session

from ..models.alert import Alert, AlertCategory, AlertSeverity, AlertStatus, AlertType
from ..models.system_metric import SystemMetric
from ..schemas import (
    AlertAcknowledge,
    AlertCreate,
    AlertFilter,
    AlertResolve,
    AlertResponse,
    AlertStatistics,
)


class AlertService:
    """Service for managing alerts with escalation, grouping, and notification features."""

    def __init__(self, db: Session):
        self.db = db

    def create_alert(self, alert_data: AlertCreate) -> AlertResponse:
        """Create a new alert."""
        existing_alert = self._find_similar_alert(alert_data)

        if existing_alert:
            existing_alert.occurrence_count += 1
            existing_alert.last_occurrence = datetime.utcnow()
            self.db.commit()
            self.db.refresh(existing_alert)
            return AlertResponse.model_validate(existing_alert)

        alert = Alert(**alert_data.model_dump())
        alert.group_key = self._generate_group_key(alert_data)

        self.db.add(alert)
        self.db.commit()
        self.db.refresh(alert)

        return AlertResponse.model_validate(alert)

    def create_metric_alert(
        self,
        metric: SystemMetric,
        alert_type: AlertType,
        title: str,
        description: str,
        recommendation: Optional[str] = None,
    ) -> AlertResponse:
        """Create an alert based on a metric threshold violation."""
        severity = (
            AlertSeverity.CRITICAL if metric.is_above_critical else AlertSeverity.HIGH
        )

        alert_data = AlertCreate(
            alert_type=alert_type,
            severity=severity,
            category=self._metric_category_to_alert_category(metric.category),
            title=title,
            description=description,
            recommendation=recommendation,
            source_module=metric.module,
            source_component=metric.component,
            source_metric_id=metric.id,
            province=metric.province,
            municipality=metric.municipality,
            trigger_conditions={
                "metric_name": metric.metric_name,
                "metric_value": metric.value,
                "metric_unit": metric.unit.value,
                "warning_threshold": metric.warning_threshold,
                "critical_threshold": metric.critical_threshold,
            },
            alert_data={
                "metric_type": metric.metric_type.value,
                "timestamp": metric.timestamp.isoformat(),
            },
            tags=metric.tags or {},
        )

        return self.create_alert(alert_data)

    def get_alerts(self, filters: AlertFilter) -> List[AlertResponse]:
        """Get alerts with filtering and pagination."""
        query = self.db.query(Alert)

        if filters.alert_type:
            query = query.filter(Alert.alert_type == filters.alert_type)
        if filters.severity:
            query = query.filter(Alert.severity == filters.severity)
        if filters.category:
            query = query.filter(Alert.category == filters.category)
        if filters.status:
            query = query.filter(Alert.status == filters.status)
        if filters.source_module:
            query = query.filter(Alert.source_module == filters.source_module)
        if filters.source_component:
            query = query.filter(Alert.source_component == filters.source_component)
        if filters.province:
            query = query.filter(Alert.province == filters.province)
        if filters.municipality:
            query = query.filter(Alert.municipality == filters.municipality)
        if filters.start_date:
            query = query.filter(Alert.created_at >= filters.start_date)
        if filters.end_date:
            query = query.filter(Alert.created_at <= filters.end_date)
        if filters.is_active is not None:
            if filters.is_active:
                query = query.filter(Alert.status == AlertStatus.ACTIVE)
            else:
                query = query.filter(Alert.status != AlertStatus.ACTIVE)
        if filters.is_critical is not None:
            if filters.is_critical:
                query = query.filter(Alert.severity == AlertSeverity.CRITICAL)
        if filters.is_overdue is not None:
            if filters.is_overdue:
                pass
        if filters.acknowledged_by:
            query = query.filter(Alert.acknowledged_by == filters.acknowledged_by)
        if filters.resolved_by:
            query = query.filter(Alert.resolved_by == filters.resolved_by)

        query = query.order_by(Alert.severity.desc(), desc(Alert.created_at))
        query = query.offset(filters.offset).limit(filters.limit)

        alerts = query.all()
        return [AlertResponse.model_validate(alert) for alert in alerts]

    def get_alert_by_id(self, alert_id: int) -> Optional[AlertResponse]:
        alert = self.db.query(Alert).filter(Alert.id == alert_id).first()
        return AlertResponse.model_validate(alert) if alert else None

    def acknowledge_alert(
        self, alert_id: int, user_id: int, acknowledge_data: AlertAcknowledge
    ) -> Optional[AlertResponse]:
        alert = self.db.query(Alert).filter(Alert.id == alert_id).first()
        if not alert or alert.status != AlertStatus.ACTIVE:
            return None

        alert.status = AlertStatus.ACKNOWLEDGED
        alert.acknowledged_at = datetime.utcnow()
        alert.acknowledged_by = user_id

        if acknowledge_data.notes:
            alert.resolution_notes = acknowledge_data.notes

        self.db.commit()
        self.db.refresh(alert)

        return AlertResponse.model_validate(alert)

    def resolve_alert(
        self, alert_id: int, user_id: int, resolve_data: AlertResolve
    ) -> Optional[AlertResponse]:
        alert = self.db.query(Alert).filter(Alert.id == alert_id).first()
        if not alert or alert.status == AlertStatus.RESOLVED:
            return None

        alert.status = AlertStatus.RESOLVED
        alert.resolved_at = datetime.utcnow()
        alert.resolved_by = user_id
        alert.resolution_notes = resolve_data.resolution_notes

        self.db.commit()
        self.db.refresh(alert)

        return AlertResponse.model_validate(alert)

    def suppress_alert(
        self, alert_id: int, suppress_until: Optional[datetime] = None
    ) -> Optional[AlertResponse]:
        alert = self.db.query(Alert).filter(Alert.id == alert_id).first()
        if not alert:
            return None

        alert.status = AlertStatus.SUPPRESSED
        alert.is_suppressed = True
        alert.suppressed_until = suppress_until or (
            datetime.utcnow() + timedelta(hours=24)
        )

        self.db.commit()
        self.db.refresh(alert)

        return AlertResponse.model_validate(alert)

    def escalate_alert(self, alert_id: int) -> Optional[AlertResponse]:
        alert = self.db.query(Alert).filter(Alert.id == alert_id).first()
        if not alert:
            return None

        alert.status = AlertStatus.ESCALATED
        alert.escalation_level += 1

        if alert.severity != AlertSeverity.CRITICAL:
            severity_order = [
                AlertSeverity.LOW,
                AlertSeverity.MEDIUM,
                AlertSeverity.HIGH,
                AlertSeverity.CRITICAL,
            ]
            current_index = severity_order.index(alert.severity)
            if current_index < len(severity_order) - 1:
                alert.severity = severity_order[current_index + 1]

        self.db.commit()
        self.db.refresh(alert)

        return AlertResponse.model_validate(alert)

    def get_active_alerts(self, limit: int = 100) -> List[AlertResponse]:
        alerts = (
            self.db.query(Alert)
            .filter(Alert.status == AlertStatus.ACTIVE)
            .order_by(Alert.severity.desc(), desc(Alert.created_at))
            .limit(limit)
            .all()
        )
        return [AlertResponse.model_validate(alert) for alert in alerts]

    def get_critical_alerts(self, limit: int = 50) -> List[AlertResponse]:
        alerts = (
            self.db.query(Alert)
            .filter(
                and_(
                    Alert.severity == AlertSeverity.CRITICAL,
                    Alert.status.in_([AlertStatus.ACTIVE, AlertStatus.ESCALATED]),
                )
            )
            .order_by(desc(Alert.created_at))
            .limit(limit)
            .all()
        )
        return [AlertResponse.model_validate(alert) for alert in alerts]

    def get_overdue_alerts(self) -> List[AlertResponse]:
        current_time = datetime.utcnow()
        sla_thresholds = {
            AlertSeverity.CRITICAL: 15,
            AlertSeverity.HIGH: 60,
            AlertSeverity.MEDIUM: 240,
            AlertSeverity.LOW: 1440,
        }

        overdue_alerts = []
        for severity, threshold_minutes in sla_thresholds.items():
            threshold_time = current_time - timedelta(minutes=threshold_minutes)
            alerts = (
                self.db.query(Alert)
                .filter(
                    and_(
                        Alert.severity == severity,
                        Alert.status == AlertStatus.ACTIVE,
                        Alert.created_at <= threshold_time,
                    )
                )
                .all()
            )
            overdue_alerts.extend(alerts)

        return [AlertResponse.model_validate(alert) for alert in overdue_alerts]

    def get_alert_statistics(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> AlertStatistics:
        query = self.db.query(Alert)
        if start_date:
            query = query.filter(Alert.created_at >= start_date)
        if end_date:
            query = query.filter(Alert.created_at <= end_date)

        all_alerts = query.all()
        total_alerts = len(all_alerts)
        active_alerts = sum(
            1 for alert in all_alerts if alert.status == AlertStatus.ACTIVE
        )
        critical_alerts = sum(
            1 for alert in all_alerts if alert.severity == AlertSeverity.CRITICAL
        )

        alerts_by_severity = {
            severity.value: sum(1 for alert in all_alerts if alert.severity == severity)
            for severity in AlertSeverity
        }
        alerts_by_category = {
            category.value: sum(1 for alert in all_alerts if alert.category == category)
            for category in AlertCategory
        }
        alerts_by_status = {
            status.value: sum(1 for alert in all_alerts if alert.status == status)
            for status in AlertStatus
        }

        resolved_alerts = [alert for alert in all_alerts if alert.resolved_at]
        if resolved_alerts:
            resolution_times = [
                (alert.resolved_at - alert.created_at).total_seconds() / 60
                for alert in resolved_alerts
            ]
            avg_resolution_time = sum(resolution_times) / len(resolution_times)
        else:
            avg_resolution_time = None

        overdue_alerts = len(self.get_overdue_alerts())

        return AlertStatistics(
            total_alerts=total_alerts,
            active_alerts=active_alerts,
            critical_alerts=critical_alerts,
            alerts_by_severity=alerts_by_severity,
            alerts_by_category=alerts_by_category,
            alerts_by_status=alerts_by_status,
            average_resolution_time_minutes=avg_resolution_time,
            overdue_alerts=overdue_alerts,
        )

    def process_metric_thresholds(self) -> List[AlertResponse]:
        recent_time = datetime.utcnow() - timedelta(minutes=5)

        threshold_violations = (
            self.db.query(SystemMetric)
            .filter(
                and_(
                    SystemMetric.timestamp >= recent_time,
                    or_(
                        and_(
                            SystemMetric.critical_threshold.isnot(None),
                            SystemMetric.value > SystemMetric.critical_threshold,
                        ),
                        and_(
                            SystemMetric.warning_threshold.isnot(None),
                            SystemMetric.value > SystemMetric.warning_threshold,
                        ),
                    ),
                )
            )
            .all()
        )

        created_alerts = []
        for metric in threshold_violations:
            existing_alert = (
                self.db.query(Alert)
                .filter(
                    and_(
                        Alert.source_metric_id == metric.id,
                        Alert.status.in_(
                            [AlertStatus.ACTIVE, AlertStatus.ACKNOWLEDGED]
                        ),
                    )
                )
                .first()
            )
            if existing_alert:
                continue

            if metric.is_above_critical:
                alert_type = (
                    AlertType.HIGH_CPU_USAGE
                    if metric.metric_type.value == "cpu_usage"
                    else AlertType.HIGH_ERROR_RATE
                )
                title = f"Critical threshold exceeded: {metric.metric_name}"
                description = (
                    f"Metric {metric.metric_name} has exceeded critical threshold. "
                    f"Current value: {metric.value} {metric.unit.value}, "
                    f"Threshold: {metric.critical_threshold}"
                )
            else:
                alert_type = (
                    AlertType.SLOW_RESPONSE_TIME
                    if "response" in metric.metric_name.lower()
                    else AlertType.HIGH_ERROR_RATE
                )
                title = f"Warning threshold exceeded: {metric.metric_name}"
                description = (
                    f"Metric {metric.metric_name} has exceeded warning threshold. "
                    f"Current value: {metric.value} {metric.unit.value}, "
                    f"Threshold: {metric.warning_threshold}"
                )

            recommendation = self._get_metric_recommendation(metric)

            alert = self.create_metric_alert(
                metric=metric,
                alert_type=alert_type,
                title=title,
                description=description,
                recommendation=recommendation,
            )
            created_alerts.append(alert)

        return created_alerts

    def cleanup_old_alerts(self, retention_days: int = 90) -> int:
        cutoff_date = datetime.utcnow() - timedelta(days=retention_days)

        deleted_count = (
            self.db.query(Alert)
            .filter(
                and_(
                    Alert.created_at < cutoff_date,
                    Alert.status == AlertStatus.RESOLVED,
                    Alert.severity != AlertSeverity.CRITICAL,
                )
            )
            .delete()
        )

        self.db.commit()
        return deleted_count

    def _find_similar_alert(self, alert_data: AlertCreate) -> Optional[Alert]:
        group_key = self._generate_group_key(alert_data)
        return (
            self.db.query(Alert)
            .filter(
                and_(
                    Alert.group_key == group_key,
                    Alert.status.in_([AlertStatus.ACTIVE, AlertStatus.ACKNOWLEDGED]),
                    Alert.created_at
                    >= datetime.utcnow() - timedelta(hours=1),  # last hour
                )
            )
            .first()
        )

    def _generate_group_key(self, alert_data: AlertCreate) -> str:
        components = [
            alert_data.alert_type.value,
            alert_data.source_module or "",
            alert_data.source_component or "",
            alert_data.affected_resource_type or "",
        ]
        return "|".join(components)

    def _metric_category_to_alert_category(self, metric_category) -> AlertCategory:
        mapping = {
            "performance": AlertCategory.APPLICATION,
            "usage": AlertCategory.APPLICATION,
            "business": AlertCategory.BUSINESS,
            "security": AlertCategory.SECURITY,
            "infrastructure": AlertCategory.INFRASTRUCTURE,
            "application": AlertCategory.APPLICATION,
        }
        return mapping.get(metric_category.value, AlertCategory.APPLICATION)

    def _get_metric_recommendation(self, metric: SystemMetric) -> str:
        recommendations = {
            "cpu_usage": "Check for resource-intensive processes and consider scaling up or optimizing code.",
            "memory_usage": "Review memory leaks, optimize queries, or increase available memory.",
            "response_time": "Optimize database queries, add caching, or scale infrastructure.",
            "error_rate": "Check application logs for errors and fix underlying issues.",
            "disk_usage": "Clean up old files, archive data, or increase disk capacity.",
            "database_connections": "Optimize connection pooling or increase connection limits.",
        }
        return recommendations.get(
            metric.metric_type.value,
            "Investigate the issue and take appropriate action.",
        )
