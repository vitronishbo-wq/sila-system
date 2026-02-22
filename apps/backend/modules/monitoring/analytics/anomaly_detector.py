"""Anomaly detection system for monitoring metrics."""

import statistics
import warnings
from datetime import datetime, timedelta
from typing import Any, Dict, List, Tuple

import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sqlalchemy.orm import Session

warnings.filterwarnings("ignore")

from ..models.alert import AlertCategory, AlertSeverity, AlertType
from ..services.alert_service import AlertService
from ..services.metric_service import MetricService


class AnomalyDetector:
    """Advanced anomaly detection system for system metrics."""

    def __init__(self, db: Session):
        self.db = db
        self.metric_service = MetricService(db)
        self.alert_service = AlertService(db)
        self.isolation_forest = IsolationForest(contamination=0.1, random_state=42)
        self.scaler = StandardScaler()

    def detect_metric_anomalies(
        self, metric_name: str, lookback_hours: int = 24, sensitivity: float = 2.0
    ) -> List[Dict[str, Any]]:
        """Detect anomalies in a specific metric using statistical methods."""
        # Get historical data
        start_time = datetime.utcnow() - timedelta(hours=lookback_hours)

        from ..schemas import SystemMetricFilter

        filters = SystemMetricFilter(
            metric_name=metric_name, start_date=start_time, limit=1000, offset=0
        )

        metrics = self.metric_service.get_metrics(filters)

        if len(metrics) < 10:  # Need minimum data points
            return []

        # Extract values and timestamps
        values = [m.value for m in metrics]
        timestamps = [m.timestamp for m in metrics]

        # Statistical anomaly detection
        anomalies = []

        # Method 1: Z-score based detection
        z_score_anomalies = self._detect_zscore_anomalies(
            values, timestamps, sensitivity
        )
        anomalies.extend(z_score_anomalies)

        # Method 2: Interquartile range (IQR) based detection
        iqr_anomalies = self._detect_iqr_anomalies(values, timestamps)
        anomalies.extend(iqr_anomalies)

        # Method 3: Moving average deviation
        ma_anomalies = self._detect_moving_average_anomalies(values, timestamps)
        anomalies.extend(ma_anomalies)

        # Remove duplicates and sort by timestamp
        unique_anomalies = self._deduplicate_anomalies(anomalies)

        return sorted(unique_anomalies, key=lambda x: x["timestamp"])

    def detect_multivariate_anomalies(
        self, metric_names: List[str], lookback_hours: int = 24
    ) -> List[Dict[str, Any]]:
        """Detect anomalies across multiple correlated metrics."""
        # Collect data for all metrics
        metric_data = {}
        start_time = datetime.utcnow() - timedelta(hours=lookback_hours)

        for metric_name in metric_names:
            from ..schemas import SystemMetricFilter

            filters = SystemMetricFilter(
                metric_name=metric_name, start_date=start_time, limit=1000, offset=0
            )

            metrics = self.metric_service.get_metrics(filters)
            metric_data[metric_name] = {
                "values": [m.value for m in metrics],
                "timestamps": [m.timestamp for m in metrics],
            }

        # Align timestamps and create feature matrix
        feature_matrix, aligned_timestamps = self._align_metric_data(metric_data)

        if len(feature_matrix) < 20:  # Need minimum data points
            return []

        # Use Isolation Forest for multivariate anomaly detection
        try:
            # Normalize features
            normalized_features = self.scaler.fit_transform(feature_matrix)

            # Detect anomalies
            anomaly_scores = self.isolation_forest.fit_predict(normalized_features)
            outlier_scores = self.isolation_forest.decision_function(
                normalized_features
            )

            # Extract anomalies
            anomalies = []
            for i, (is_anomaly, score) in enumerate(
                zip(anomaly_scores, outlier_scores)
            ):
                if is_anomaly == -1:  # Anomaly detected
                    anomalies.append(
                        {
                            "timestamp": aligned_timestamps[i],
                            "anomaly_score": abs(score),
                            "affected_metrics": metric_names,
                            "values": {
                                name: feature_matrix[i][j]
                                for j, name in enumerate(metric_names)
                            },
                            "detection_method": "isolation_forest",
                            "severity": self._calculate_anomaly_severity(abs(score)),
                        }
                    )

            return anomalies

        except Exception as e:
            # Fallback to statistical methods if ML fails
            return self._fallback_multivariate_detection(metric_data)

    def detect_pattern_anomalies(
        self, metric_name: str, pattern_type: str = "seasonal", lookback_days: int = 7
    ) -> List[Dict[str, Any]]:
        """Detect anomalies in metric patterns (seasonal, trend, etc.)."""
        start_time = datetime.utcnow() - timedelta(days=lookback_days)

        filters = SystemMetricFilter(
            metric_name=metric_name, start_date=start_time, limit=2000, offset=0
        )

        metrics = self.metric_service.get_metrics(filters)

        if len(metrics) < 50:  # Need sufficient data for pattern analysis
            return []

        values = [m.value for m in metrics]
        timestamps = [m.timestamp for m in metrics]

        anomalies = []

        if pattern_type == "seasonal":
            anomalies = self._detect_seasonal_anomalies(values, timestamps)
        elif pattern_type == "trend":
            anomalies = self._detect_trend_anomalies(values, timestamps)
        elif pattern_type == "cyclical":
            anomalies = self._detect_cyclical_anomalies(values, timestamps)

        return anomalies

    def detect_threshold_anomalies(
        self, lookback_hours: int = 1
    ) -> List[Dict[str, Any]]:
        """Detect metrics that have crossed their defined thresholds."""
        start_time = datetime.utcnow() - timedelta(hours=lookback_hours)

        filters = SystemMetricFilter(start_date=start_time, limit=1000, offset=0)

        metrics = self.metric_service.get_metrics(filters)

        threshold_anomalies = []

        for metric in metrics:
            anomaly_info = None

            # Check critical threshold
            if metric.critical_threshold and metric.value > metric.critical_threshold:
                anomaly_info = {
                    "metric_id": metric.id,
                    "metric_name": metric.metric_name,
                    "timestamp": metric.timestamp,
                    "value": metric.value,
                    "threshold_type": "critical",
                    "threshold_value": metric.critical_threshold,
                    "severity": "critical",
                    "deviation": metric.value - metric.critical_threshold,
                    "deviation_percentage": (
                        (metric.value - metric.critical_threshold)
                        / metric.critical_threshold
                    )
                    * 100,
                }

            # Check warning threshold
            elif metric.warning_threshold and metric.value > metric.warning_threshold:
                anomaly_info = {
                    "metric_id": metric.id,
                    "metric_name": metric.metric_name,
                    "timestamp": metric.timestamp,
                    "value": metric.value,
                    "threshold_type": "warning",
                    "threshold_value": metric.warning_threshold,
                    "severity": "warning",
                    "deviation": metric.value - metric.warning_threshold,
                    "deviation_percentage": (
                        (metric.value - metric.warning_threshold)
                        / metric.warning_threshold
                    )
                    * 100,
                }

            if anomaly_info:
                threshold_anomalies.append(anomaly_info)

        return threshold_anomalies

    def create_anomaly_alerts(
        self, anomalies: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Create alerts for detected anomalies."""
        created_alerts = []

        for anomaly in anomalies:
            # Determine alert type based on anomaly characteristics
            alert_type = self._determine_alert_type(anomaly)
            severity = self._map_severity(anomaly.get("severity", "medium"))

            # Create alert
            from ..schemas import AlertCreate

            alert_data = AlertCreate(
                alert_type=alert_type,
                severity=severity,
                category=AlertCategory.APPLICATION,
                title=f"Anomaly detected: {anomaly.get('metric_name', 'Unknown metric')}",
                description=self._generate_anomaly_description(anomaly),
                recommendation=self._generate_anomaly_recommendation(anomaly),
                source_module="monitoring",
                source_component="anomaly_detector",
                alert_data=anomaly,
            )

            try:
                alert = self.alert_service.create_alert(alert_data)
                created_alerts.append(alert.model_dump())
            except Exception as e:
                # Log error but continue processing other anomalies
                continue

        return created_alerts

    def get_anomaly_summary(self, lookback_hours: int = 24) -> Dict[str, Any]:
        """Get summary of anomalies detected in the specified time period."""
        start_time = datetime.utcnow() - timedelta(hours=lookback_hours)

        # Get metrics marked as anomalies

        filters = SystemMetricFilter(
            start_date=start_time, is_anomaly=True, limit=1000, offset=0
        )

        anomalous_metrics = self.metric_service.get_metrics(filters)

        # Analyze anomalies
        summary = {
            "total_anomalies": len(anomalous_metrics),
            "time_period_hours": lookback_hours,
            "anomalies_by_metric": {},
            "anomalies_by_module": {},
            "anomalies_by_severity": {"low": 0, "medium": 0, "high": 0, "critical": 0},
            "most_anomalous_metrics": [],
            "anomaly_rate": 0.0,
        }

        # Count by metric name
        for metric in anomalous_metrics:
            metric_name = metric.metric_name
            summary["anomalies_by_metric"][metric_name] = (
                summary["anomalies_by_metric"].get(metric_name, 0) + 1
            )

        # Count by module
        for metric in anomalous_metrics:
            module = metric.module or "unknown"
            summary["anomalies_by_module"][module] = (
                summary["anomalies_by_module"].get(module, 0) + 1
            )

        # Calculate anomaly rate
        total_metrics_filters = SystemMetricFilter(
            start_date=start_time, limit=10000, offset=0
        )
        total_metrics = self.metric_service.get_metrics(total_metrics_filters)

        if total_metrics:
            summary["anomaly_rate"] = (
                len(anomalous_metrics) / len(total_metrics)
            ) * 100

        # Most anomalous metrics
        summary["most_anomalous_metrics"] = sorted(
            summary["anomalies_by_metric"].items(), key=lambda x: x[1], reverse=True
        )[:10]

        return summary

    # ============================================================================
    # PRIVATE HELPER METHODS
    # ============================================================================

    def _detect_zscore_anomalies(
        self, values: List[float], timestamps: List[datetime], sensitivity: float = 2.0
    ) -> List[Dict[str, Any]]:
        """Detect anomalies using Z-score method."""
        if len(values) < 3:
            return []

        mean_val = statistics.mean(values)
        std_val = statistics.stdev(values)

        if std_val == 0:
            return []

        anomalies = []
        for i, (value, timestamp) in enumerate(zip(values, timestamps)):
            z_score = abs(value - mean_val) / std_val

            if z_score > sensitivity:
                anomalies.append(
                    {
                        "timestamp": timestamp,
                        "value": value,
                        "z_score": z_score,
                        "detection_method": "z_score",
                        "severity": "high" if z_score > 3.0 else "medium",
                    }
                )

        return anomalies

    def _detect_iqr_anomalies(
        self, values: List[float], timestamps: List[datetime]
    ) -> List[Dict[str, Any]]:
        """Detect anomalies using Interquartile Range method."""
        if len(values) < 4:
            return []

        sorted_values = sorted(values)
        n = len(sorted_values)

        q1 = sorted_values[n // 4]
        q3 = sorted_values[3 * n // 4]
        iqr = q3 - q1

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        anomalies = []
        for value, timestamp in zip(values, timestamps):
            if value < lower_bound or value > upper_bound:
                anomalies.append(
                    {
                        "timestamp": timestamp,
                        "value": value,
                        "lower_bound": lower_bound,
                        "upper_bound": upper_bound,
                        "detection_method": "iqr",
                        "severity": "medium",
                    }
                )

        return anomalies

    def _detect_moving_average_anomalies(
        self,
        values: List[float],
        timestamps: List[datetime],
        window_size: int = 10,
        threshold: float = 2.0,
    ) -> List[Dict[str, Any]]:
        """Detect anomalies using moving average deviation."""
        if len(values) < window_size * 2:
            return []

        anomalies = []

        for i in range(window_size, len(values)):
            # Calculate moving average and standard deviation
            window_values = values[i - window_size : i]
            moving_avg = statistics.mean(window_values)
            moving_std = (
                statistics.stdev(window_values) if len(window_values) > 1 else 0
            )

            if moving_std == 0:
                continue

            # Check if current value deviates significantly
            deviation = abs(values[i] - moving_avg) / moving_std

            if deviation > threshold:
                anomalies.append(
                    {
                        "timestamp": timestamps[i],
                        "value": values[i],
                        "moving_average": moving_avg,
                        "deviation": deviation,
                        "detection_method": "moving_average",
                        "severity": "high" if deviation > 3.0 else "medium",
                    }
                )

        return anomalies

    def _detect_seasonal_anomalies(
        self, values: List[float], timestamps: List[datetime]
    ) -> List[Dict[str, Any]]:
        """Detect seasonal pattern anomalies."""
        # Simple seasonal detection based on hour of day patterns
        hourly_patterns = {}

        # Build hourly patterns
        for value, timestamp in zip(values, timestamps):
            hour = timestamp.hour
            if hour not in hourly_patterns:
                hourly_patterns[hour] = []
            hourly_patterns[hour].append(value)

        # Calculate expected ranges for each hour
        hourly_ranges = {}
        for hour, hour_values in hourly_patterns.items():
            if len(hour_values) >= 3:
                mean_val = statistics.mean(hour_values)
                std_val = statistics.stdev(hour_values)
                hourly_ranges[hour] = {
                    "mean": mean_val,
                    "std": std_val,
                    "lower": mean_val - 2 * std_val,
                    "upper": mean_val + 2 * std_val,
                }

        # Detect anomalies
        anomalies = []
        for value, timestamp in zip(values, timestamps):
            hour = timestamp.hour
            if hour in hourly_ranges:
                range_info = hourly_ranges[hour]
                if value < range_info["lower"] or value > range_info["upper"]:
                    anomalies.append(
                        {
                            "timestamp": timestamp,
                            "value": value,
                            "expected_range": range_info,
                            "detection_method": "seasonal",
                            "severity": "medium",
                        }
                    )

        return anomalies

    def _detect_trend_anomalies(
        self, values: List[float], timestamps: List[datetime]
    ) -> List[Dict[str, Any]]:
        """Detect trend-based anomalies."""
        if len(values) < 10:
            return []

        # Calculate trend using linear regression
        x = list(range(len(values)))
        n = len(values)

        sum_x = sum(x)
        sum_y = sum(values)
        sum_xy = sum(xi * yi for xi, yi in zip(x, values))
        sum_x2 = sum(xi * xi for xi in x)

        # Linear regression coefficients
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
        intercept = (sum_y - slope * sum_x) / n

        # Calculate residuals and detect anomalies
        anomalies = []
        residuals = []

        for i, (value, timestamp) in enumerate(zip(values, timestamps)):
            expected = slope * i + intercept
            residual = abs(value - expected)
            residuals.append(residual)

        # Use residuals to detect anomalies
        if len(residuals) > 1:
            residual_mean = statistics.mean(residuals)
            residual_std = statistics.stdev(residuals)

            for i, (residual, timestamp, value) in enumerate(
                zip(residuals, timestamps, values)
            ):
                if residual_std > 0 and residual > residual_mean + 2 * residual_std:
                    anomalies.append(
                        {
                            "timestamp": timestamp,
                            "value": value,
                            "expected_value": slope * i + intercept,
                            "residual": residual,
                            "detection_method": "trend",
                            "severity": "medium",
                        }
                    )

        return anomalies

    def _detect_cyclical_anomalies(
        self, values: List[float], timestamps: List[datetime]
    ) -> List[Dict[str, Any]]:
        """Detect cyclical pattern anomalies."""
        # Simple cyclical detection based on day of week patterns
        daily_patterns = {}

        # Build daily patterns
        for value, timestamp in zip(values, timestamps):
            day = timestamp.weekday()  # 0=Monday, 6=Sunday
            if day not in daily_patterns:
                daily_patterns[day] = []
            daily_patterns[day].append(value)

        # Calculate expected ranges for each day
        daily_ranges = {}
        for day, day_values in daily_patterns.items():
            if len(day_values) >= 3:
                mean_val = statistics.mean(day_values)
                std_val = statistics.stdev(day_values)
                daily_ranges[day] = {
                    "mean": mean_val,
                    "std": std_val,
                    "lower": mean_val - 2 * std_val,
                    "upper": mean_val + 2 * std_val,
                }

        # Detect anomalies
        anomalies = []
        for value, timestamp in zip(values, timestamps):
            day = timestamp.weekday()
            if day in daily_ranges:
                range_info = daily_ranges[day]
                if value < range_info["lower"] or value > range_info["upper"]:
                    anomalies.append(
                        {
                            "timestamp": timestamp,
                            "value": value,
                            "expected_range": range_info,
                            "detection_method": "cyclical",
                            "severity": "medium",
                        }
                    )

        return anomalies

    def _align_metric_data(
        self, metric_data: Dict[str, Dict[str, List]]
    ) -> Tuple[List[List[float]], List[datetime]]:
        """Align multiple metrics by timestamp for multivariate analysis."""
        # Find common timestamps
        all_timestamps = set()
        for data in metric_data.values():
            all_timestamps.update(data["timestamps"])

        common_timestamps = sorted(all_timestamps)

        # Create feature matrix
        feature_matrix = []
        aligned_timestamps = []

        for timestamp in common_timestamps:
            row = []
            has_all_metrics = True

            for metric_name in metric_data.keys():
                timestamps = metric_data[metric_name]["timestamps"]
                values = metric_data[metric_name]["values"]

                # Find closest timestamp
                closest_idx = None
                min_diff = float("inf")

                for i, ts in enumerate(timestamps):
                    diff = abs((ts - timestamp).total_seconds())
                    if diff < min_diff:
                        min_diff = diff
                        closest_idx = i

                if closest_idx is not None and min_diff < 300:  # Within 5 minutes
                    row.append(values[closest_idx])
                else:
                    has_all_metrics = False
                    break

            if has_all_metrics:
                feature_matrix.append(row)
                aligned_timestamps.append(timestamp)

        return feature_matrix, aligned_timestamps

    def _fallback_multivariate_detection(
        self, metric_data: Dict[str, Dict[str, List]]
    ) -> List[Dict[str, Any]]:
        """Fallback multivariate anomaly detection using correlation analysis."""
        anomalies = []

        # Simple correlation-based detection
        metric_names = list(metric_data.keys())

        for i, metric1 in enumerate(metric_names):
            for j, metric2 in enumerate(metric_names[i + 1 :], i + 1):
                # Calculate correlation between metrics
                values1 = metric_data[metric1]["values"]
                values2 = metric_data[metric2]["values"]

                if len(values1) == len(values2) and len(values1) > 10:
                    try:
                        correlation = np.corrcoef(values1, values2)[0, 1]

                        # If correlation is strong, look for deviations
                        if abs(correlation) > 0.7:
                            # Simple deviation detection
                            for k, (v1, v2, ts1) in enumerate(
                                zip(
                                    values1, values2, metric_data[metric1]["timestamps"]
                                )
                            ):
                                expected_v2 = correlation * v1
                                deviation = abs(v2 - expected_v2)

                                if deviation > statistics.stdev(values2):
                                    anomalies.append(
                                        {
                                            "timestamp": ts1,
                                            "affected_metrics": [metric1, metric2],
                                            "values": {metric1: v1, metric2: v2},
                                            "expected_correlation": correlation,
                                            "deviation": deviation,
                                            "detection_method": "correlation",
                                            "severity": "medium",
                                        }
                                    )
                    except:
                        continue

        return anomalies

    def _deduplicate_anomalies(
        self, anomalies: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Remove duplicate anomalies based on timestamp proximity."""
        if not anomalies:
            return []

        # Sort by timestamp
        sorted_anomalies = sorted(anomalies, key=lambda x: x["timestamp"])

        deduplicated = [sorted_anomalies[0]]

        for anomaly in sorted_anomalies[1:]:
            # Check if this anomaly is too close to the last one
            time_diff = (
                anomaly["timestamp"] - deduplicated[-1]["timestamp"]
            ).total_seconds()

            if time_diff > 300:  # More than 5 minutes apart
                deduplicated.append(anomaly)

        return deduplicated

    def _calculate_anomaly_severity(self, score: float) -> str:
        """Calculate severity based on anomaly score."""
        if score > 0.8:
            return "critical"
        elif score > 0.6:
            return "high"
        elif score > 0.4:
            return "medium"
        else:
            return "low"

    def _determine_alert_type(self, anomaly: Dict[str, Any]) -> AlertType:
        """Determine alert type based on anomaly characteristics."""
        metric_name = anomaly.get("metric_name", "").lower()

        if "response_time" in metric_name:
            return AlertType.SLOW_RESPONSE_TIME
        elif "error" in metric_name:
            return AlertType.HIGH_ERROR_RATE
        elif "cpu" in metric_name:
            return AlertType.HIGH_CPU_USAGE
        elif "memory" in metric_name:
            return AlertType.HIGH_MEMORY_USAGE
        elif "traffic" in metric_name or "request" in metric_name:
            return AlertType.UNUSUAL_TRAFFIC_PATTERN
        else:
            return AlertType.UNEXPECTED_DATA_VOLUME

    def _map_severity(self, severity_str: str) -> AlertSeverity:
        """Map severity string to AlertSeverity enum."""
        mapping = {
            "low": AlertSeverity.LOW,
            "medium": AlertSeverity.MEDIUM,
            "high": AlertSeverity.HIGH,
            "critical": AlertSeverity.CRITICAL,
        }
        return mapping.get(severity_str.lower(), AlertSeverity.MEDIUM)

    def _generate_anomaly_description(self, anomaly: Dict[str, Any]) -> str:
        """Generate human-readable anomaly description."""
        method = anomaly.get("detection_method", "unknown")
        metric_name = anomaly.get("metric_name", "unknown metric")
        value = anomaly.get("value", 0)

        if method == "z_score":
            z_score = anomaly.get("z_score", 0)
            return f"Metric {metric_name} value {value} deviates significantly from normal (Z-score: {z_score:.2f})"
        elif method == "iqr":
            return f"Metric {metric_name} value {value} is outside normal range (IQR-based detection)"
        elif method == "threshold":
            threshold_type = anomaly.get("threshold_type", "unknown")
            threshold_value = anomaly.get("threshold_value", 0)
            return f"Metric {metric_name} value {value} exceeded {threshold_type} threshold of {threshold_value}"
        else:
            return f"Anomaly detected in {metric_name}: value {value} using {method} method"

    def _generate_anomaly_recommendation(self, anomaly: Dict[str, Any]) -> str:
        """Generate recommendation based on anomaly type."""
        metric_name = anomaly.get("metric_name", "").lower()

        if "response_time" in metric_name:
            return "Check for slow database queries, optimize code performance, or scale infrastructure"
        elif "error" in metric_name:
            return (
                "Review application logs for error patterns and fix underlying issues"
            )
        elif "cpu" in metric_name:
            return "Investigate high CPU usage processes and consider scaling or optimization"
        elif "memory" in metric_name:
            return "Check for memory leaks and optimize memory usage or increase available memory"
        elif "disk" in metric_name:
            return "Clean up disk space or increase storage capacity"
        else:
            return (
                "Investigate the anomaly cause and take appropriate corrective action"
            )
