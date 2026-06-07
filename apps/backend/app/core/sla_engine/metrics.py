from __future__ import annotations

try:
    from prometheus_client import Counter, Gauge, Histogram
except Exception:
    Counter = None
    Histogram = None
    Gauge = None


if Counter and Histogram and Gauge:
    sla_calculations = Counter(
        "sla_calculations_total",
        "Total de cálculos de SLA",
        ["service_id", "status"],
    )
    sla_calculation_duration = Histogram(
        "sla_calculation_duration_seconds",
        "Duração do cálculo de SLA",
        buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1],
    )
    sla_violations = Counter(
        "sla_violations_total",
        "Total de violações de SLA",
        ["service_id", "province", "severity"],
    )
    sla_current = Gauge(
        "sla_current_hours",
        "SLA atual por serviço",
        ["service_id", "province", "citizen_type"],
    )
    sla_breach_probability = Gauge(
        "sla_breach_probability",
        "Probabilidade de violação",
        ["service_id"],
    )
else:
    sla_calculations = None
    sla_calculation_duration = None
    sla_violations = None
    sla_current = None
    sla_breach_probability = None


class SLAMetrics:
    """Coletor de métricas de SLA"""

    @staticmethod
    def record_calculation(service_id: str, result: float, error: bool = False) -> None:
        _ = result
        status = "error" if error else "success"
        if sla_calculations:
            sla_calculations.labels(service_id=service_id, status=status).inc()

    @staticmethod
    def record_calculation_time(duration: float) -> None:
        if sla_calculation_duration:
            sla_calculation_duration.observe(duration)

    @staticmethod
    def record_violation(service_id: str, province: str | None, severity: str) -> None:
        if sla_violations:
            sla_violations.labels(
                service_id=service_id,
                province=province or "unknown",
                severity=severity,
            ).inc()

    @staticmethod
    def update_current_sla(service_id: str, hours: float, province: str, citizen_type: str) -> None:
        if sla_current:
            sla_current.labels(
                service_id=service_id, province=province, citizen_type=citizen_type
            ).set(hours)

    @staticmethod
    def update_breach_probability(service_id: str, probability: float) -> None:
        if sla_breach_probability:
            sla_breach_probability.labels(service_id=service_id).set(probability)

    @staticmethod
    def record_batch_calculation(total: int) -> None:
        if sla_calculations:
            sla_calculations.labels(service_id="batch", status="success").inc(total)
