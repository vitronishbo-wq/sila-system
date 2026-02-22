"""Performance monitoring integration for the monitoring module."""

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import psutil
from sqlalchemy.orm import Session

from ..models.alert import AlertCategory, AlertSeverity, AlertType
from ..models.system_metric import MetricCategory, MetricType, MetricUnit
from ..services.alert_service import AlertService
from ..services.metric_service import MetricService


class PerformanceMonitor:
    """Performance monitoring service for system metrics and alerts."""

    def __init__(self, db: Session):
        self.db = db
        self.metric_service = MetricService(db)
        self.alert_service = AlertService(db)

    def collect_system_metrics(self):
        """Collect and record system performance metrics."""
        timestamp = datetime.utcnow()

        # CPU metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        self.metric_service.record_metric(
            metric_name="system_cpu_usage",
            metric_type=MetricType.CPU_USAGE,
            category=MetricCategory.INFRASTRUCTURE,
            value=cpu_percent,
            unit=MetricUnit.PERCENTAGE,
            module="system",
            component="performance_monitor",
            warning_threshold=70.0,
            critical_threshold=90.0,
        )

        # Memory metrics
        memory = psutil.virtual_memory()
        self.metric_service.record_metric(
            metric_name="system_memory_usage",
            metric_type=MetricType.MEMORY_USAGE,
            category=MetricCategory.INFRASTRUCTURE,
            value=memory.percent,
            unit=MetricUnit.PERCENTAGE,
            module="system",
            component="performance_monitor",
            warning_threshold=80.0,
            critical_threshold=95.0,
        )

        # Disk metrics
        disk = psutil.disk_usage("/")
        disk_percent = (disk.used / disk.total) * 100
        self.metric_service.record_metric(
            metric_name="system_disk_usage",
            metric_type=MetricType.DISK_USAGE,
            category=MetricCategory.INFRASTRUCTURE,
            value=disk_percent,
            unit=MetricUnit.PERCENTAGE,
            module="system",
            component="performance_monitor",
            warning_threshold=80.0,
            critical_threshold=95.0,
        )

        # Network metrics (if available)
        try:
            network = psutil.net_io_counters()
            self.metric_service.record_metric(
                metric_name="network_bytes_sent",
                metric_type=MetricType.THROUGHPUT,
                category=MetricCategory.INFRASTRUCTURE,
                value=network.bytes_sent,
                unit=MetricUnit.BYTES,
                module="system",
                component="performance_monitor",
            )

            self.metric_service.record_metric(
                metric_name="network_bytes_received",
                metric_type=MetricType.THROUGHPUT,
                category=MetricCategory.INFRASTRUCTURE,
                value=network.bytes_recv,
                unit=MetricUnit.BYTES,
                module="system",
                component="performance_monitor",
            )
        except:
            pass  # Network metrics not available

    def record_request_metrics(
        self,
        endpoint: str,
        method: str,
        response_time_ms: float,
        status_code: int,
        user_id: Optional[int] = None,
        province: Optional[str] = None,
        municipality: Optional[str] = None,
    ):
        """Record HTTP request performance metrics."""
        # Response time metric
        self.metric_service.record_metric(
            metric_name=f"request_response_time_{method.lower()}",
            metric_type=MetricType.RESPONSE_TIME,
            category=MetricCategory.PERFORMANCE,
            value=response_time_ms,
            unit=MetricUnit.MILLISECONDS,
            module="api",
            component="request_handler",
            province=province,
            municipality=municipality,
            warning_threshold=2000.0,  # 2 seconds
            critical_threshold=5000.0,  # 5 seconds
            metadata={
                "endpoint": endpoint,
                "method": method,
                "status_code": status_code,
                "user_id": user_id,
            },
        )

        # Request count metric
        self.metric_service.record_metric(
            metric_name="api_requests_total",
            metric_type=MetricType.API_CALLS,
            category=MetricCategory.USAGE,
            value=1,
            unit=MetricUnit.COUNT,
            module="api",
            component="request_handler",
            province=province,
            municipality=municipality,
            metadata={
                "endpoint": endpoint,
                "method": method,
                "status_code": status_code,
            },
        )

        # Error rate metric (if error)
        if status_code >= 400:
            self.metric_service.record_metric(
                metric_name="api_errors_total",
                metric_type=MetricType.ERROR_RATE,
                category=MetricCategory.PERFORMANCE,
                value=1,
                unit=MetricUnit.COUNT,
                module="api",
                component="request_handler",
                province=province,
                municipality=municipality,
                metadata={
                    "endpoint": endpoint,
                    "method": method,
                    "status_code": status_code,
                    "error_type": self._classify_error(status_code),
                },
            )

    def record_database_metrics(
        self,
        operation: str,
        table_name: str,
        execution_time_ms: float,
        rows_affected: int = 0,
        success: bool = True,
    ):
        """Record database operation performance metrics."""
        # Database response time
        self.metric_service.record_metric(
            metric_name=f"db_{operation}_time",
            metric_type=MetricType.RESPONSE_TIME,
            category=MetricCategory.PERFORMANCE,
            value=execution_time_ms,
            unit=MetricUnit.MILLISECONDS,
            module="database",
            component="db_handler",
            warning_threshold=1000.0,  # 1 second
            critical_threshold=3000.0,  # 3 seconds
            metadata={
                "operation": operation,
                "table_name": table_name,
                "rows_affected": rows_affected,
                "success": success,
            },
        )

        # Database operation count
        self.metric_service.record_metric(
            metric_name=f"db_{operation}_count",
            metric_type=MetricType.API_CALLS,
            category=MetricCategory.USAGE,
            value=1,
            unit=MetricUnit.COUNT,
            module="database",
            component="db_handler",
            metadata={
                "operation": operation,
                "table_name": table_name,
                "success": success,
            },
        )

        # Database error count (if failed)
        if not success:
            self.metric_service.record_metric(
                metric_name="db_errors_total",
                metric_type=MetricType.ERROR_RATE,
                category=MetricCategory.PERFORMANCE,
                value=1,
                unit=MetricUnit.COUNT,
                module="database",
                component="db_handler",
                metadata={"operation": operation, "table_name": table_name},
            )

    def record_business_metrics(
        self,
        metric_name: str,
        value: float,
        unit: MetricUnit,
        module: str,
        operation_type: str,
        province: Optional[str] = None,
        municipality: Optional[str] = None,
        additional_metadata: Optional[Dict[str, Any]] = None,
    ):
        """Record business-specific performance metrics."""
        metadata = {"operation_type": operation_type, **(additional_metadata or {})}

        self.metric_service.record_metric(
            metric_name=metric_name,
            metric_type=self._get_business_metric_type(operation_type),
            category=MetricCategory.BUSINESS,
            value=value,
            unit=unit,
            module=module,
            component="business_service",
            province=province,
            municipality=municipality,
            metadata=metadata,
        )

    def monitor_service_health(
        self,
        service_name: str,
        module: str,
        is_healthy: bool,
        response_time_ms: Optional[float] = None,
        error_message: Optional[str] = None,
    ):
        """Monitor individual service health status."""
        # Service availability metric
        availability_value = 1.0 if is_healthy else 0.0
        self.metric_service.record_metric(
            metric_name=f"service_availability_{service_name}",
            metric_type=MetricType.AVAILABILITY,
            category=MetricCategory.APPLICATION,
            value=availability_value,
            unit=MetricUnit.PERCENTAGE,
            module=module,
            component=service_name,
            critical_threshold=0.5,  # Alert if availability drops below 50%
            metadata={
                "service_name": service_name,
                "is_healthy": is_healthy,
                "error_message": error_message,
            },
        )

        # Service response time (if available)
        if response_time_ms is not None:
            self.metric_service.record_metric(
                metric_name=f"service_response_time_{service_name}",
                metric_type=MetricType.RESPONSE_TIME,
                category=MetricCategory.PERFORMANCE,
                value=response_time_ms,
                unit=MetricUnit.MILLISECONDS,
                module=module,
                component=service_name,
                warning_threshold=1000.0,
                critical_threshold=3000.0,
            )

        # Create alert if service is unhealthy
        if not is_healthy:
            self._create_service_health_alert(service_name, module, error_message)

    def calculate_sla_metrics(
        self, service_name: str, time_period_hours: int = 24
    ) -> Dict[str, Any]:
        """Calculate SLA metrics for a service."""
        start_time = datetime.utcnow() - timedelta(hours=time_period_hours)

        # Get availability metrics
        from ..schemas import SystemMetricFilter

        availability_filters = SystemMetricFilter(
            metric_name=f"service_availability_{service_name}",
            start_date=start_time,
            limit=1000,
            offset=0,
        )

        availability_metrics = self.metric_service.get_metrics(availability_filters)

        if not availability_metrics:
            return {
                "service_name": service_name,
                "time_period_hours": time_period_hours,
                "availability_percentage": 0,
                "uptime_minutes": 0,
                "downtime_minutes": 0,
                "sla_target": 99.9,
                "sla_met": False,
            }

        # Calculate availability percentage
        total_checks = len(availability_metrics)
        successful_checks = sum(1 for m in availability_metrics if m.value == 1.0)
        availability_percentage = (
            (successful_checks / total_checks) * 100 if total_checks > 0 else 0
        )

        # Calculate uptime/downtime
        uptime_minutes = (
            (successful_checks / total_checks) * (time_period_hours * 60)
            if total_checks > 0
            else 0
        )
        downtime_minutes = (time_period_hours * 60) - uptime_minutes

        # SLA target (configurable)
        sla_target = 99.9
        sla_met = availability_percentage >= sla_target

        return {
            "service_name": service_name,
            "time_period_hours": time_period_hours,
            "availability_percentage": round(availability_percentage, 2),
            "uptime_minutes": round(uptime_minutes, 2),
            "downtime_minutes": round(downtime_minutes, 2),
            "total_checks": total_checks,
            "successful_checks": successful_checks,
            "sla_target": sla_target,
            "sla_met": sla_met,
        }

    def get_performance_summary(self, time_period_hours: int = 24) -> Dict[str, Any]:
        """Get comprehensive performance summary."""
        start_time = datetime.utcnow() - timedelta(hours=time_period_hours)

        # Get system health metrics
        system_health = self.metric_service.get_system_health_metrics()

        # Get response time statistics

        response_time_filters = SystemMetricFilter(
            metric_type=MetricType.RESPONSE_TIME,
            start_date=start_time,
            limit=1000,
            offset=0,
        )

        response_time_metrics = self.metric_service.get_metrics(response_time_filters)

        if response_time_metrics:
            response_times = [m.value for m in response_time_metrics]
            avg_response_time = sum(response_times) / len(response_times)
            max_response_time = max(response_times)
            min_response_time = min(response_times)
        else:
            avg_response_time = max_response_time = min_response_time = 0

        # Get error rate statistics
        error_filters = SystemMetricFilter(
            metric_type=MetricType.ERROR_RATE,
            start_date=start_time,
            limit=1000,
            offset=0,
        )

        error_metrics = self.metric_service.get_metrics(error_filters)
        total_errors = sum(m.value for m in error_metrics)

        # Get request count
        request_filters = SystemMetricFilter(
            metric_name="api_requests_total",
            start_date=start_time,
            limit=1000,
            offset=0,
        )

        request_metrics = self.metric_service.get_metrics(request_filters)
        total_requests = sum(m.value for m in request_metrics)

        # Calculate error rate percentage
        error_rate_percentage = (
            (total_errors / total_requests * 100) if total_requests > 0 else 0
        )

        return {
            "time_period_hours": time_period_hours,
            "system_health": system_health,
            "performance_metrics": {
                "avg_response_time_ms": round(avg_response_time, 2),
                "max_response_time_ms": round(max_response_time, 2),
                "min_response_time_ms": round(min_response_time, 2),
                "total_requests": int(total_requests),
                "total_errors": int(total_errors),
                "error_rate_percentage": round(error_rate_percentage, 2),
                "requests_per_hour": (
                    round(total_requests / time_period_hours, 2)
                    if time_period_hours > 0
                    else 0
                ),
            },
            "thresholds": {
                "response_time_warning_ms": 2000,
                "response_time_critical_ms": 5000,
                "error_rate_warning_percentage": 5,
                "error_rate_critical_percentage": 10,
            },
            "status": self._determine_performance_status(
                avg_response_time, error_rate_percentage
            ),
        }

    def detect_performance_anomalies(self):
        """Detect performance anomalies and create alerts."""
        # Get recent metrics for anomaly detection
        recent_time = datetime.utcnow() - timedelta(minutes=15)

        filters = SystemMetricFilter(
            start_date=recent_time, is_anomaly=True, limit=100, offset=0
        )

        anomalous_metrics = self.metric_service.get_metrics(filters)

        # Group anomalies by type and create alerts
        anomaly_groups = {}
        for metric in anomalous_metrics:
            key = f"{metric.metric_type.value}_{metric.module}"
            if key not in anomaly_groups:
                anomaly_groups[key] = []
            anomaly_groups[key].append(metric)

        # Create alerts for significant anomaly groups
        alerts_created = []
        for group_key, metrics in anomaly_groups.items():
            if len(metrics) >= 3:  # Multiple anomalies in short time
                alert = self._create_performance_anomaly_alert(group_key, metrics)
                alerts_created.append(alert)

        return alerts_created

    # ============================================================================
    # PRIVATE HELPER METHODS
    # ============================================================================

    def _classify_error(self, status_code: int) -> str:
        """Classify HTTP error by status code."""
        if 400 <= status_code < 500:
            return "client_error"
        elif 500 <= status_code < 600:
            return "server_error"
        else:
            return "unknown_error"

    def _get_business_metric_type(self, operation_type: str) -> MetricType:
        """Map business operation to metric type."""
        mapping = {
            "citizen_registration": MetricType.CITIZEN_REGISTRATIONS,
            "document_request": MetricType.DOCUMENT_REQUESTS,
            "payment": MetricType.PAYMENT_TRANSACTIONS,
            "case_submission": MetricType.CASE_SUBMISSIONS,
            "appointment": MetricType.API_CALLS,
            "login": MetricType.LOGIN_ATTEMPTS,
        }

        return mapping.get(operation_type, MetricType.API_CALLS)

    def _create_service_health_alert(
        self, service_name: str, module: str, error_message: Optional[str]
    ):
        """Create alert for service health issues."""
        from ..schemas import AlertCreate

        alert_data = AlertCreate(
            alert_type=AlertType.SERVICE_UNAVAILABLE,
            severity=AlertSeverity.HIGH,
            category=AlertCategory.APPLICATION,
            title=f"Service health issue: {service_name}",
            description=f"Service {service_name} in module {module} is unhealthy",
            recommendation=f"Check service logs and restart {service_name} if necessary",
            source_module=module,
            source_component=service_name,
            alert_data={
                "service_name": service_name,
                "error_message": error_message,
                "health_check": "failed",
            },
        )

        return self.alert_service.create_alert(alert_data)

    def _create_performance_anomaly_alert(self, group_key: str, metrics: List):
        """Create alert for performance anomalies."""

        metric_type, module = group_key.split("_", 1)

        alert_data = AlertCreate(
            alert_type=AlertType.UNUSUAL_TRAFFIC_PATTERN,
            severity=AlertSeverity.MEDIUM,
            category=AlertCategory.APPLICATION,
            title=f"Performance anomaly detected: {metric_type}",
            description=f"Multiple anomalous {metric_type} metrics detected in {module} module",
            recommendation="Investigate the cause of performance anomalies and take corrective action",
            source_module=module,
            source_component="performance_monitor",
            alert_data={
                "anomaly_count": len(metrics),
                "metric_type": metric_type,
                "time_window": "15_minutes",
            },
        )

        return self.alert_service.create_alert(alert_data)

    def _determine_performance_status(
        self, avg_response_time: float, error_rate_percentage: float
    ) -> str:
        """Determine overall performance status."""
        if avg_response_time > 5000 or error_rate_percentage > 10:
            return "critical"
        elif avg_response_time > 2000 or error_rate_percentage > 5:
            return "warning"
        else:
            return "good"
