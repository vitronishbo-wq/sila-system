"""Pattern analysis for monitoring data."""

import statistics
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Any, Dict, List

from sqlalchemy.orm import Session

from ..models.audit_log import AuditLog
from ..models.system_metric import SystemMetric
from ..services.audit_service import AuditService
from ..services.metric_service import MetricService


class PatternAnalyzer:
    """Advanced pattern analysis for monitoring data."""

    def __init__(self, db: Session):
        self.db = db
        self.metric_service = MetricService(db)
        self.audit_service = AuditService(db)

    def analyze_metric_trends(
        self, metric_name: str, lookback_days: int = 7
    ) -> Dict[str, Any]:
        """Analyze trends in metric data over time."""
        start_time = datetime.utcnow() - timedelta(days=lookback_days)

        from ..schemas import SystemMetricFilter

        filters = SystemMetricFilter(
            metric_name=metric_name, start_date=start_time, limit=2000, offset=0
        )

        metrics = self.metric_service.get_metrics(filters)

        if len(metrics) < 10:
            return {"error": "Insufficient data for trend analysis"}

        # Extract values and timestamps
        values = [m.value for m in metrics]
        timestamps = [m.timestamp for m in metrics]

        # Calculate trend statistics
        trend_analysis = {
            "metric_name": metric_name,
            "period_days": lookback_days,
            "data_points": len(metrics),
            "trend_direction": self._calculate_trend_direction(values),
            "trend_strength": self._calculate_trend_strength(values),
            "volatility": self._calculate_volatility(values),
            "seasonal_patterns": self._detect_seasonal_patterns(values, timestamps),
            "outliers": self._detect_outliers(values, timestamps),
            "statistics": {
                "mean": statistics.mean(values),
                "median": statistics.median(values),
                "std_dev": statistics.stdev(values) if len(values) > 1 else 0,
                "min": min(values),
                "max": max(values),
                "range": max(values) - min(values),
            },
        }

        return trend_analysis

    def analyze_usage_patterns(self, lookback_days: int = 30) -> Dict[str, Any]:
        """Analyze system usage patterns."""
        start_time = datetime.utcnow() - timedelta(days=lookback_days)

        # Get audit logs for usage analysis
        from ..schemas import AuditLogFilter

        audit_filters = AuditLogFilter(start_date=start_time, limit=5000, offset=0)

        audit_logs = self.audit_service.get_audit_logs(audit_filters)

        # Analyze patterns
        usage_patterns = {
            "period_days": lookback_days,
            "total_activities": len(audit_logs),
            "hourly_distribution": self._analyze_hourly_distribution(audit_logs),
            "daily_distribution": self._analyze_daily_distribution(audit_logs),
            "module_usage": self._analyze_module_usage(audit_logs),
            "user_activity": self._analyze_user_activity(audit_logs),
            "peak_hours": self._identify_peak_hours(audit_logs),
            "activity_trends": self._analyze_activity_trends(audit_logs),
        }

        return usage_patterns

    def analyze_error_patterns(self, lookback_days: int = 7) -> Dict[str, Any]:
        """Analyze error patterns in the system."""
        start_time = datetime.utcnow() - timedelta(days=lookback_days)

        # Get error-related audit logs

        filters = AuditLogFilter(
            start_date=start_time, action="ERROR", limit=2000, offset=0
        )

        error_logs = self.audit_service.get_audit_logs(filters)

        error_patterns = {
            "period_days": lookback_days,
            "total_errors": len(error_logs),
            "error_frequency": self._calculate_error_frequency(error_logs),
            "error_types": self._categorize_errors(error_logs),
            "error_sources": self._analyze_error_sources(error_logs),
            "error_trends": self._analyze_error_trends(error_logs),
        }

        return error_patterns

    def analyze_performance_patterns(self, lookback_days: int = 7) -> Dict[str, Any]:
        """Analyze system performance patterns."""
        start_time = datetime.utcnow() - timedelta(days=lookback_days)

        # Get performance-related metrics
        performance_metrics = [
            "response_time",
            "cpu_usage",
            "memory_usage",
            "disk_usage",
            "network_throughput",
        ]

        performance_data = {}
        for metric_type in performance_metrics:
            from ..schemas import SystemMetricFilter

            filters = SystemMetricFilter(start_date=start_time, limit=1000, offset=0)

            metrics = self.metric_service.get_metrics(filters)
            relevant_metrics = [
                m for m in metrics if metric_type in m.metric_name.lower()
            ]

            if relevant_metrics:
                performance_data[metric_type] = relevant_metrics

        performance_patterns = {
            "period_days": lookback_days,
            "metrics_analyzed": list(performance_data.keys()),
            "performance_summary": self._summarize_performance(performance_data),
            "bottlenecks": self._identify_bottlenecks(performance_data),
            "performance_trends": self._analyze_performance_trends(performance_data),
            "recommendations": self._generate_performance_recommendations(
                performance_data
            ),
        }

        return performance_patterns

    def detect_anomalous_patterns(
        self, metric_name: str, lookback_days: int = 14
    ) -> Dict[str, Any]:
        """Detect anomalous patterns in metric data."""
        start_time = datetime.utcnow() - timedelta(days=lookback_days)

        filters = SystemMetricFilter(
            metric_name=metric_name, start_date=start_time, limit=2000, offset=0
        )

        metrics = self.metric_service.get_metrics(filters)

        if len(metrics) < 20:
            return {"error": "Insufficient data for anomaly pattern detection"}

        values = [m.value for m in metrics]
        timestamps = [m.timestamp for m in metrics]

        anomaly_patterns = {
            "metric_name": metric_name,
            "period_days": lookback_days,
            "data_points": len(metrics),
            "spike_patterns": self._detect_spike_patterns(values, timestamps),
            "dip_patterns": self._detect_dip_patterns(values, timestamps),
            "oscillation_patterns": self._detect_oscillation_patterns(
                values, timestamps
            ),
            "drift_patterns": self._detect_drift_patterns(values, timestamps),
            "anomaly_score": self._calculate_overall_anomaly_score(values),
            "pattern_recommendations": self._generate_pattern_recommendations(
                values, timestamps
            ),
        }

        return anomaly_patterns

    # ============================================================================
    # PRIVATE HELPER METHODS
    # ============================================================================

    def _calculate_trend_direction(self, values: List[float]) -> str:
        """Calculate overall trend direction."""
        if len(values) < 2:
            return "unknown"

        # Simple linear regression slope
        n = len(values)
        x = list(range(n))

        sum_x = sum(x)
        sum_y = sum(values)
        sum_xy = sum(xi * yi for xi, yi in zip(x, values))
        sum_x2 = sum(xi * xi for xi in x)

        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)

        if slope > 0.1:
            return "increasing"
        elif slope < -0.1:
            return "decreasing"
        else:
            return "stable"

    def _calculate_trend_strength(self, values: List[float]) -> float:
        """Calculate strength of trend (0-1)."""
        if len(values) < 3:
            return 0.0

        # Calculate R-squared for linear trend
        n = len(values)
        x = list(range(n))

        # Linear regression
        sum_x = sum(x)
        sum_y = sum(values)
        sum_xy = sum(xi * yi for xi, yi in zip(x, values))
        sum_x2 = sum(xi * xi for xi in x)

        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
        intercept = (sum_y - slope * sum_x) / n

        # Calculate R-squared
        y_mean = sum_y / n
        ss_tot = sum((yi - y_mean) ** 2 for yi in values)
        ss_res = sum((yi - (slope * xi + intercept)) ** 2 for xi, yi in zip(x, values))

        if ss_tot == 0:
            return 0.0

        r_squared = 1 - (ss_res / ss_tot)
        return max(0.0, min(1.0, r_squared))

    def _calculate_volatility(self, values: List[float]) -> float:
        """Calculate volatility (coefficient of variation)."""
        if len(values) < 2:
            return 0.0

        mean_val = statistics.mean(values)
        if mean_val == 0:
            return 0.0

        std_val = statistics.stdev(values)
        return std_val / mean_val

    def _detect_seasonal_patterns(
        self, values: List[float], timestamps: List[datetime]
    ) -> Dict[str, Any]:
        """Detect seasonal patterns in data."""
        if len(values) < 24:  # Need at least 24 hours of data
            return {"detected": False}

        # Group by hour of day
        hourly_data = defaultdict(list)
        for value, timestamp in zip(values, timestamps):
            hour = timestamp.hour
            hourly_data[hour].append(value)

        # Calculate hourly averages
        hourly_averages = {}
        for hour, hour_values in hourly_data.items():
            if len(hour_values) >= 2:
                hourly_averages[hour] = statistics.mean(hour_values)

        if len(hourly_averages) < 12:  # Need data for at least half the day
            return {"detected": False}

        # Check for significant variation across hours
        avg_values = list(hourly_averages.values())
        overall_mean = statistics.mean(avg_values)
        variation = max(avg_values) - min(avg_values)

        seasonal_strength = variation / overall_mean if overall_mean > 0 else 0

        return {
            "detected": seasonal_strength > 0.2,
            "strength": seasonal_strength,
            "hourly_pattern": hourly_averages,
            "peak_hour": (
                max(hourly_averages, key=hourly_averages.get)
                if hourly_averages
                else None
            ),
            "low_hour": (
                min(hourly_averages, key=hourly_averages.get)
                if hourly_averages
                else None
            ),
        }

    def _detect_outliers(
        self, values: List[float], timestamps: List[datetime]
    ) -> List[Dict[str, Any]]:
        """Detect outliers in the data."""
        if len(values) < 4:
            return []

        # Use IQR method
        sorted_values = sorted(values)
        n = len(sorted_values)

        q1 = sorted_values[n // 4]
        q3 = sorted_values[3 * n // 4]
        iqr = q3 - q1

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        outliers = []
        for value, timestamp in zip(values, timestamps):
            if value < lower_bound or value > upper_bound:
                outliers.append(
                    {
                        "timestamp": timestamp.isoformat(),
                        "value": value,
                        "type": "high" if value > upper_bound else "low",
                        "deviation": abs(value - (q1 + q3) / 2),
                    }
                )

        return outliers

    def _analyze_hourly_distribution(
        self, audit_logs: List[AuditLog]
    ) -> Dict[int, int]:
        """Analyze activity distribution by hour."""
        hourly_counts = defaultdict(int)

        for log in audit_logs:
            hour = log.timestamp.hour
            hourly_counts[hour] += 1

        return dict(hourly_counts)

    def _analyze_daily_distribution(self, audit_logs: List[AuditLog]) -> Dict[int, int]:
        """Analyze activity distribution by day of week."""
        daily_counts = defaultdict(int)

        for log in audit_logs:
            day = log.timestamp.weekday()  # 0=Monday, 6=Sunday
            daily_counts[day] += 1

        return dict(daily_counts)

    def _analyze_module_usage(self, audit_logs: List[AuditLog]) -> Dict[str, int]:
        """Analyze usage by module."""
        module_counts = defaultdict(int)

        for log in audit_logs:
            module = log.module or "unknown"
            module_counts[module] += 1

        return dict(module_counts)

    def _analyze_user_activity(self, audit_logs: List[AuditLog]) -> Dict[str, Any]:
        """Analyze user activity patterns."""
        user_counts = defaultdict(int)
        unique_users = set()

        for log in audit_logs:
            if log.user_id:
                user_counts[str(log.user_id)] += 1
                unique_users.add(log.user_id)

        return {
            "unique_users": len(unique_users),
            "total_activities": sum(user_counts.values()),
            "avg_activities_per_user": (
                sum(user_counts.values()) / len(unique_users) if unique_users else 0
            ),
            "most_active_users": sorted(
                user_counts.items(), key=lambda x: x[1], reverse=True
            )[:10],
        }

    def _identify_peak_hours(self, audit_logs: List[AuditLog]) -> List[int]:
        """Identify peak activity hours."""
        hourly_counts = self._analyze_hourly_distribution(audit_logs)

        if not hourly_counts:
            return []

        avg_activity = sum(hourly_counts.values()) / len(hourly_counts)
        peak_threshold = avg_activity * 1.5

        peak_hours = [
            hour for hour, count in hourly_counts.items() if count >= peak_threshold
        ]
        return sorted(peak_hours)

    def _analyze_activity_trends(self, audit_logs: List[AuditLog]) -> Dict[str, Any]:
        """Analyze activity trends over time."""
        if not audit_logs:
            return {}

        # Group by day
        daily_counts = defaultdict(int)
        for log in audit_logs:
            day = log.timestamp.date()
            daily_counts[day] += 1

        # Calculate trend
        sorted_days = sorted(daily_counts.keys())
        daily_values = [daily_counts[day] for day in sorted_days]

        if len(daily_values) < 2:
            return {"trend": "insufficient_data"}

        trend_direction = self._calculate_trend_direction(daily_values)

        return {
            "trend": trend_direction,
            "daily_average": statistics.mean(daily_values),
            "peak_day": (
                max(daily_counts, key=daily_counts.get) if daily_counts else None
            ),
            "low_day": (
                min(daily_counts, key=daily_counts.get) if daily_counts else None
            ),
        }

    def _calculate_error_frequency(
        self, error_logs: List[AuditLog]
    ) -> Dict[str, float]:
        """Calculate error frequency statistics."""
        if not error_logs:
            return {}

        # Group by day
        daily_errors = defaultdict(int)
        for log in error_logs:
            day = log.timestamp.date()
            daily_errors[day] += 1

        daily_counts = list(daily_errors.values())

        return {
            "daily_average": statistics.mean(daily_counts) if daily_counts else 0,
            "daily_max": max(daily_counts) if daily_counts else 0,
            "daily_min": min(daily_counts) if daily_counts else 0,
            "total_error_days": len(daily_errors),
        }

    def _categorize_errors(self, error_logs: List[AuditLog]) -> Dict[str, int]:
        """Categorize errors by type."""
        error_categories = defaultdict(int)

        for log in error_logs:
            # Simple categorization based on description
            description = (log.description or "").lower()

            if "database" in description or "sql" in description:
                error_categories["database"] += 1
            elif "network" in description or "connection" in description:
                error_categories["network"] += 1
            elif "authentication" in description or "auth" in description:
                error_categories["authentication"] += 1
            elif "validation" in description:
                error_categories["validation"] += 1
            elif "permission" in description or "access" in description:
                error_categories["permission"] += 1
            else:
                error_categories["other"] += 1

        return dict(error_categories)

    def _analyze_error_sources(self, error_logs: List[AuditLog]) -> Dict[str, int]:
        """Analyze error sources by module."""
        source_counts = defaultdict(int)

        for log in error_logs:
            module = log.module or "unknown"
            source_counts[module] += 1

        return dict(source_counts)

    def _analyze_error_trends(self, error_logs: List[AuditLog]) -> Dict[str, Any]:
        """Analyze error trends over time."""
        return self._analyze_activity_trends(error_logs)

    def _summarize_performance(
        self, performance_data: Dict[str, List[SystemMetric]]
    ) -> Dict[str, Any]:
        """Summarize performance across all metrics."""
        summary = {}

        for metric_type, metrics in performance_data.items():
            if metrics:
                values = [m.value for m in metrics]
                summary[metric_type] = {
                    "average": statistics.mean(values),
                    "max": max(values),
                    "min": min(values),
                    "std_dev": statistics.stdev(values) if len(values) > 1 else 0,
                    "data_points": len(values),
                }

        return summary

    def _identify_bottlenecks(
        self, performance_data: Dict[str, List[SystemMetric]]
    ) -> List[str]:
        """Identify performance bottlenecks."""
        bottlenecks = []

        # Simple threshold-based bottleneck detection
        thresholds = {
            "cpu_usage": 80,
            "memory_usage": 85,
            "disk_usage": 90,
            "response_time": 2000,
        }

        for metric_type, metrics in performance_data.items():
            if metrics and metric_type in thresholds:
                values = [m.value for m in metrics]
                avg_value = statistics.mean(values)

                if avg_value > thresholds[metric_type]:
                    bottlenecks.append(
                        f"{metric_type}: {avg_value:.1f} (threshold: {thresholds[metric_type]})"
                    )

        return bottlenecks

    def _analyze_performance_trends(
        self, performance_data: Dict[str, List[SystemMetric]]
    ) -> Dict[str, str]:
        """Analyze performance trends."""
        trends = {}

        for metric_type, metrics in performance_data.items():
            if metrics and len(metrics) >= 5:
                values = [m.value for m in metrics]
                trend = self._calculate_trend_direction(values)
                trends[metric_type] = trend

        return trends

    def _generate_performance_recommendations(
        self, performance_data: Dict[str, List[SystemMetric]]
    ) -> List[str]:
        """Generate performance improvement recommendations."""
        recommendations = []

        bottlenecks = self._identify_bottlenecks(performance_data)

        for bottleneck in bottlenecks:
            if "cpu_usage" in bottleneck:
                recommendations.append("Consider CPU optimization or scaling")
            elif "memory_usage" in bottleneck:
                recommendations.append(
                    "Investigate memory usage and consider increasing available memory"
                )
            elif "disk_usage" in bottleneck:
                recommendations.append(
                    "Clean up disk space or increase storage capacity"
                )
            elif "response_time" in bottleneck:
                recommendations.append(
                    "Optimize application performance and database queries"
                )

        if not recommendations:
            recommendations.append("Performance metrics are within normal ranges")

        return recommendations

    def _detect_spike_patterns(
        self, values: List[float], timestamps: List[datetime]
    ) -> List[Dict[str, Any]]:
        """Detect spike patterns in data."""
        if len(values) < 10:
            return []

        spikes = []
        mean_val = statistics.mean(values)
        std_val = statistics.stdev(values) if len(values) > 1 else 0

        if std_val == 0:
            return []

        spike_threshold = mean_val + 3 * std_val

        for i, (value, timestamp) in enumerate(zip(values, timestamps)):
            if value > spike_threshold:
                spikes.append(
                    {
                        "timestamp": timestamp.isoformat(),
                        "value": value,
                        "deviation": value - mean_val,
                        "severity": (
                            "high" if value > mean_val + 4 * std_val else "medium"
                        ),
                    }
                )

        return spikes

    def _detect_dip_patterns(
        self, values: List[float], timestamps: List[datetime]
    ) -> List[Dict[str, Any]]:
        """Detect dip patterns in data."""
        if len(values) < 10:
            return []

        dips = []
        mean_val = statistics.mean(values)
        std_val = statistics.stdev(values) if len(values) > 1 else 0

        if std_val == 0:
            return []

        dip_threshold = mean_val - 3 * std_val

        for value, timestamp in zip(values, timestamps):
            if value < dip_threshold:
                dips.append(
                    {
                        "timestamp": timestamp.isoformat(),
                        "value": value,
                        "deviation": mean_val - value,
                        "severity": (
                            "high" if value < mean_val - 4 * std_val else "medium"
                        ),
                    }
                )

        return dips

    def _detect_oscillation_patterns(
        self, values: List[float], timestamps: List[datetime]
    ) -> Dict[str, Any]:
        """Detect oscillation patterns in data."""
        if len(values) < 20:
            return {"detected": False}

        # Simple oscillation detection based on direction changes
        direction_changes = 0

        for i in range(2, len(values)):
            prev_diff = values[i - 1] - values[i - 2]
            curr_diff = values[i] - values[i - 1]

            if (prev_diff > 0 and curr_diff < 0) or (prev_diff < 0 and curr_diff > 0):
                direction_changes += 1

        # Calculate oscillation frequency
        oscillation_rate = direction_changes / len(values)

        return {
            "detected": oscillation_rate > 0.3,
            "frequency": oscillation_rate,
            "direction_changes": direction_changes,
            "severity": "high" if oscillation_rate > 0.5 else "medium",
        }

    def _detect_drift_patterns(
        self, values: List[float], timestamps: List[datetime]
    ) -> Dict[str, Any]:
        """Detect drift patterns in data."""
        if len(values) < 20:
            return {"detected": False}

        # Split data into segments and compare
        segment_size = len(values) // 4

        if segment_size < 5:
            return {"detected": False}

        first_segment = values[:segment_size]
        last_segment = values[-segment_size:]

        first_mean = statistics.mean(first_segment)
        last_mean = statistics.mean(last_segment)

        if first_mean == 0:
            return {"detected": False}

        drift_percentage = ((last_mean - first_mean) / first_mean) * 100

        return {
            "detected": abs(drift_percentage) > 20,
            "drift_percentage": drift_percentage,
            "direction": "upward" if drift_percentage > 0 else "downward",
            "severity": "high" if abs(drift_percentage) > 50 else "medium",
        }

    def _calculate_overall_anomaly_score(self, values: List[float]) -> float:
        """Calculate overall anomaly score for the data."""
        if len(values) < 5:
            return 0.0

        # Combine multiple anomaly indicators
        volatility = self._calculate_volatility(values)

        # Normalize volatility to 0-1 scale
        anomaly_score = min(1.0, volatility)

        return anomaly_score

    def _generate_pattern_recommendations(
        self, values: List[float], timestamps: List[datetime]
    ) -> List[str]:
        """Generate recommendations based on detected patterns."""
        recommendations = []

        volatility = self._calculate_volatility(values)

        if volatility > 0.5:
            recommendations.append(
                "High volatility detected - investigate causes of instability"
            )

        trend = self._calculate_trend_direction(values)
        if trend == "increasing":
            recommendations.append(
                "Increasing trend detected - monitor for potential issues"
            )
        elif trend == "decreasing":
            recommendations.append(
                "Decreasing trend detected - verify if this is expected"
            )

        if not recommendations:
            recommendations.append(
                "No significant patterns detected - continue monitoring"
            )

        return recommendations
