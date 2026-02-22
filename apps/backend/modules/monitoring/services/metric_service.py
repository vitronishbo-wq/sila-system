"""Metric service for the monitoring module."""

import statistics
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from sqlalchemy import and_, asc, desc, func
from sqlalchemy.orm import Session

from ..models.system_metric import MetricCategory, MetricType, MetricUnit, SystemMetric
from ..schemas import (
    MetricAggregation,
    SystemMetricCreate,
    SystemMetricFilter,
    SystemMetricResponse,
    SystemMetricUpdate,
)


class MetricService:
    """Service for managing system metrics with collection, aggregation, and analysis."""

    def __init__(self, db: Session):
        self.db = db

    def create_metric(self, metric_data: SystemMetricCreate) -> SystemMetricResponse:
        """Create a new system metric entry."""
        metric = SystemMetric(**metric_data.model_dump())

        self.db.add(metric)
        self.db.commit()
        self.db.refresh(metric)

        return SystemMetricResponse.model_validate(metric)

    def record_metric(
        self,
        metric_name: str,
        metric_type: MetricType,
        category: MetricCategory,
        value: float,
        unit: MetricUnit,
        module: Optional[str] = None,
        component: Optional[str] = None,
        environment: str = "production",
        province: Optional[str] = None,
        municipality: Optional[str] = None,
        tags: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        warning_threshold: Optional[float] = None,
        critical_threshold: Optional[float] = None,
    ) -> SystemMetricResponse:
        """Record a system metric with automatic anomaly detection."""
        # Check for anomalies
        is_anomaly = self._detect_anomaly(metric_name, value, metric_type)

        metric_data = SystemMetricCreate(
            metric_name=metric_name,
            metric_type=metric_type,
            category=category,
            value=value,
            unit=unit,
            module=module,
            component=component,
            environment=environment,
            province=province,
            municipality=municipality,
            tags=tags,
            metadata=metadata,
            warning_threshold=warning_threshold,
            critical_threshold=critical_threshold,
            is_anomaly=is_anomaly,
        )

        return self.create_metric(metric_data)

    def get_metrics(self, filters: SystemMetricFilter) -> List[SystemMetricResponse]:
        """Get metrics with filtering and pagination."""
        query = self.db.query(SystemMetric)

        # Apply filters
        if filters.metric_name:
            query = query.filter(
                SystemMetric.metric_name.ilike(f"%{filters.metric_name}%")
            )

        if filters.metric_type:
            query = query.filter(SystemMetric.metric_type == filters.metric_type)

        if filters.category:
            query = query.filter(SystemMetric.category == filters.category)

        if filters.module:
            query = query.filter(SystemMetric.module == filters.module)

        if filters.component:
            query = query.filter(SystemMetric.component == filters.component)

        if filters.environment:
            query = query.filter(SystemMetric.environment == filters.environment)

        if filters.province:
            query = query.filter(SystemMetric.province == filters.province)

        if filters.municipality:
            query = query.filter(SystemMetric.municipality == filters.municipality)

        if filters.start_date:
            query = query.filter(SystemMetric.timestamp >= filters.start_date)

        if filters.end_date:
            query = query.filter(SystemMetric.timestamp <= filters.end_date)

        if filters.is_anomaly is not None:
            query = query.filter(SystemMetric.is_anomaly == filters.is_anomaly)

        if filters.above_warning:
            query = query.filter(
                and_(
                    SystemMetric.warning_threshold.isnot(None),
                    SystemMetric.value > SystemMetric.warning_threshold,
                )
            )

        if filters.above_critical:
            query = query.filter(
                and_(
                    SystemMetric.critical_threshold.isnot(None),
                    SystemMetric.value > SystemMetric.critical_threshold,
                )
            )

        # Order by timestamp descending
        query = query.order_by(desc(SystemMetric.timestamp))

        # Apply pagination
        query = query.offset(filters.offset).limit(filters.limit)

        metrics = query.all()
        return [SystemMetricResponse.model_validate(metric) for metric in metrics]

    def get_metric_by_id(self, metric_id: int) -> Optional[SystemMetricResponse]:
        """Get a specific metric by ID."""
        metric = (
            self.db.query(SystemMetric).filter(SystemMetric.id == metric_id).first()
        )
        if metric:
            return SystemMetricResponse.model_validate(metric)
        return None

    def update_metric(
        self, metric_id: int, update_data: SystemMetricUpdate
    ) -> Optional[SystemMetricResponse]:
        """Update a metric's thresholds and flags."""
        metric = (
            self.db.query(SystemMetric).filter(SystemMetric.id == metric_id).first()
        )
        if not metric:
            return None

        update_dict = update_data.model_dump(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(metric, field, value)

        self.db.commit()
        self.db.refresh(metric)

        return SystemMetricResponse.model_validate(metric)

    def aggregate_metrics(self, aggregation: MetricAggregation) -> List[Dict[str, Any]]:
        """Aggregate metrics based on specified criteria."""
        query = self.db.query(SystemMetric).filter(
            SystemMetric.metric_name == aggregation.metric_name
        )

        # Apply date filters
        if aggregation.start_date:
            query = query.filter(SystemMetric.timestamp >= aggregation.start_date)

        if aggregation.end_date:
            query = query.filter(SystemMetric.timestamp <= aggregation.end_date)

        # Build aggregation query
        select_fields = []
        group_by_fields = []

        # Add grouping fields
        if aggregation.group_by:
            for field in aggregation.group_by:
                if hasattr(SystemMetric, field):
                    column = getattr(SystemMetric, field)
                    select_fields.append(column.label(field))
                    group_by_fields.append(column)

        # Add time interval grouping
        if aggregation.interval:
            time_field = self._get_time_interval_field(aggregation.interval)
            select_fields.append(time_field.label("time_interval"))
            group_by_fields.append(time_field)

        # Add aggregation function
        if aggregation.aggregation_type == "sum":
            agg_field = func.sum(SystemMetric.value).label("value")
        elif aggregation.aggregation_type == "avg":
            agg_field = func.avg(SystemMetric.value).label("value")
        elif aggregation.aggregation_type == "min":
            agg_field = func.min(SystemMetric.value).label("value")
        elif aggregation.aggregation_type == "max":
            agg_field = func.max(SystemMetric.value).label("value")
        elif aggregation.aggregation_type == "count":
            agg_field = func.count(SystemMetric.id).label("value")
        else:
            agg_field = func.avg(SystemMetric.value).label("value")

        select_fields.append(agg_field)
        select_fields.append(func.count(SystemMetric.id).label("sample_count"))

        # Execute aggregation query
        if group_by_fields:
            results = (
                query.with_entities(*select_fields)
                .group_by(*group_by_fields)
                .order_by(
                    asc("time_interval")
                    if aggregation.interval
                    else asc(group_by_fields[0])
                )
                .all()
            )
        else:
            results = query.with_entities(
                agg_field, func.count(SystemMetric.id).label("sample_count")
            ).all()

        # Convert results to dictionaries
        aggregated_data = []
        for result in results:
            result_dict = {}
            for i, field in enumerate(select_fields):
                key = field.name if hasattr(field, "name") else f"field_{i}"
                result_dict[key] = result[i]
            aggregated_data.append(result_dict)

        return aggregated_data

    def get_metric_statistics(
        self,
        metric_name: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        """Get comprehensive statistics for a specific metric."""
        query = self.db.query(SystemMetric).filter(
            SystemMetric.metric_name == metric_name
        )

        if start_date:
            query = query.filter(SystemMetric.timestamp >= start_date)

        if end_date:
            query = query.filter(SystemMetric.timestamp <= end_date)

        metrics = query.all()

        if not metrics:
            return {"error": "No data found for the specified metric"}

        values = [m.value for m in metrics]

        return {
            "metric_name": metric_name,
            "total_samples": len(values),
            "min_value": min(values),
            "max_value": max(values),
            "average": statistics.mean(values),
            "median": statistics.median(values),
            "std_deviation": statistics.stdev(values) if len(values) > 1 else 0,
            "percentiles": {
                "p50": statistics.median(values),
                "p90": self._percentile(values, 90),
                "p95": self._percentile(values, 95),
                "p99": self._percentile(values, 99),
            },
            "anomaly_count": sum(1 for m in metrics if m.is_anomaly),
            "threshold_violations": {
                "warning": sum(1 for m in metrics if m.is_above_warning),
                "critical": sum(1 for m in metrics if m.is_above_critical),
            },
            "time_range": {
                "start": min(m.timestamp for m in metrics).isoformat(),
                "end": max(m.timestamp for m in metrics).isoformat(),
            },
        }

    def get_system_health_metrics(self) -> Dict[str, Any]:
        """Get current system health metrics."""
        # Get recent metrics (last hour)
        recent_time = datetime.utcnow() - timedelta(hours=1)

        # Response time metrics
        response_time_query = self.db.query(SystemMetric).filter(
            and_(
                SystemMetric.metric_type == MetricType.RESPONSE_TIME,
                SystemMetric.timestamp >= recent_time,
            )
        )

        response_times = [m.value for m in response_time_query.all()]
        avg_response_time = statistics.mean(response_times) if response_times else 0

        # Error rate metrics
        error_rate_query = self.db.query(SystemMetric).filter(
            and_(
                SystemMetric.metric_type == MetricType.ERROR_RATE,
                SystemMetric.timestamp >= recent_time,
            )
        )

        error_rates = [m.value for m in error_rate_query.all()]
        avg_error_rate = statistics.mean(error_rates) if error_rates else 0

        # Active users
        active_users_query = (
            self.db.query(SystemMetric)
            .filter(
                and_(
                    SystemMetric.metric_type == MetricType.ACTIVE_USERS,
                    SystemMetric.timestamp >= recent_time,
                )
            )
            .order_by(desc(SystemMetric.timestamp))
            .first()
        )

        active_users = active_users_query.value if active_users_query else 0

        # CPU usage
        cpu_usage_query = (
            self.db.query(SystemMetric)
            .filter(
                and_(
                    SystemMetric.metric_type == MetricType.CPU_USAGE,
                    SystemMetric.timestamp >= recent_time,
                )
            )
            .order_by(desc(SystemMetric.timestamp))
            .first()
        )

        cpu_usage = cpu_usage_query.value if cpu_usage_query else 0

        # Memory usage
        memory_usage_query = (
            self.db.query(SystemMetric)
            .filter(
                and_(
                    SystemMetric.metric_type == MetricType.MEMORY_USAGE,
                    SystemMetric.timestamp >= recent_time,
                )
            )
            .order_by(desc(SystemMetric.timestamp))
            .first()
        )

        memory_usage = memory_usage_query.value if memory_usage_query else 0

        # Determine overall health status
        health_status = self._determine_health_status(
            avg_response_time, avg_error_rate, cpu_usage, memory_usage
        )

        return {
            "overall_status": health_status,
            "response_time_avg": avg_response_time,
            "error_rate_percentage": avg_error_rate,
            "active_users": int(active_users),
            "cpu_usage_percentage": cpu_usage,
            "memory_usage_percentage": memory_usage,
            "last_updated": datetime.utcnow().isoformat(),
        }

    def get_performance_trends(
        self, metric_names: List[str], days: int = 7
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Get performance trends for specified metrics over time."""
        start_date = datetime.utcnow() - timedelta(days=days)
        trends = {}

        for metric_name in metric_names:
            query = (
                self.db.query(SystemMetric)
                .filter(
                    and_(
                        SystemMetric.metric_name == metric_name,
                        SystemMetric.timestamp >= start_date,
                    )
                )
                .order_by(asc(SystemMetric.timestamp))
            )

            metrics = query.all()
            trend_data = []

            for metric in metrics:
                trend_data.append(
                    {
                        "timestamp": metric.timestamp.isoformat(),
                        "value": metric.value,
                        "unit": metric.unit.value,
                        "is_anomaly": metric.is_anomaly,
                    }
                )

            trends[metric_name] = trend_data

        return trends

    def cleanup_old_metrics(self, retention_days: int = 90) -> int:
        """Clean up old metrics based on retention policy."""
        cutoff_date = datetime.utcnow() - timedelta(days=retention_days)

        # Keep aggregated metrics and critical anomalies longer
        deleted_count = (
            self.db.query(SystemMetric)
            .filter(
                and_(
                    SystemMetric.timestamp < cutoff_date,
                    SystemMetric.is_aggregated == False,
                    SystemMetric.is_anomaly == False,
                )
            )
            .delete()
        )

        self.db.commit()
        return deleted_count

    def _detect_anomaly(
        self, metric_name: str, value: float, metric_type: MetricType
    ) -> bool:
        """Detect if a metric value is anomalous based on historical data."""
        # Get recent historical data (last 24 hours)
        recent_time = datetime.utcnow() - timedelta(hours=24)

        historical_query = self.db.query(SystemMetric).filter(
            and_(
                SystemMetric.metric_name == metric_name,
                SystemMetric.timestamp >= recent_time,
                SystemMetric.is_anomaly == False,
            )
        )  # Exclude previous anomalies

        historical_values = [m.value for m in historical_query.all()]

        if len(historical_values) < 10:  # Need minimum samples
            return False

        # Calculate statistical thresholds
        mean_val = statistics.mean(historical_values)
        std_dev = statistics.stdev(historical_values)

        # Define anomaly thresholds (2 standard deviations)
        upper_threshold = mean_val + (2 * std_dev)
        lower_threshold = mean_val - (2 * std_dev)

        # Some metrics should only check upper threshold
        if metric_type in [
            MetricType.ERROR_RATE,
            MetricType.RESPONSE_TIME,
            MetricType.CPU_USAGE,
            MetricType.MEMORY_USAGE,
        ]:
            return value > upper_threshold

        # Other metrics check both thresholds
        return value > upper_threshold or value < lower_threshold

    def _get_time_interval_field(self, interval: str):
        """Get SQL field for time interval grouping."""
        if interval == "minute":
            return func.date_trunc("minute", SystemMetric.timestamp)
        elif interval == "hour":
            return func.date_trunc("hour", SystemMetric.timestamp)
        elif interval == "day":
            return func.date_trunc("day", SystemMetric.timestamp)
        elif interval == "week":
            return func.date_trunc("week", SystemMetric.timestamp)
        elif interval == "month":
            return func.date_trunc("month", SystemMetric.timestamp)
        else:
            return func.date_trunc("hour", SystemMetric.timestamp)

    def _percentile(self, values: List[float], percentile: int) -> float:
        """Calculate percentile value."""
        sorted_values = sorted(values)
        index = (percentile / 100) * (len(sorted_values) - 1)

        if index.is_integer():
            return sorted_values[int(index)]
        else:
            lower_index = int(index)
            upper_index = lower_index + 1
            weight = index - lower_index
            return (
                sorted_values[lower_index] * (1 - weight)
                + sorted_values[upper_index] * weight
            )

    def _determine_health_status(
        self,
        response_time: float,
        error_rate: float,
        cpu_usage: float,
        memory_usage: float,
    ) -> str:
        """Determine overall system health status."""
        # Define thresholds
        critical_conditions = [
            response_time > 5000,  # 5 seconds
            error_rate > 10,  # 10%
            cpu_usage > 90,  # 90%
            memory_usage > 95,  # 95%
        ]

        warning_conditions = [
            response_time > 2000,  # 2 seconds
            error_rate > 5,  # 5%
            cpu_usage > 70,  # 70%
            memory_usage > 80,  # 80%
        ]

        if any(critical_conditions):
            return "critical"
        elif any(warning_conditions):
            return "warning"
        else:
            return "healthy"
