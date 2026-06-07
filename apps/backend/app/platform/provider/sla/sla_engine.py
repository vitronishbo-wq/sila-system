import logging
import statistics
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from typing import Optional

from apps.backend.app.platform.integration.provider_registry import ProviderRegistry
from apps.backend.app.platform.provider.sla.sla_metrics import SLAMetrics, SLAStatus

logger = logging.getLogger(__name__)


class SLAEngine:
    def __init__(self, window_minutes: int = 60):
        self._window_minutes = window_minutes
        self._latencies: dict[str, list[float]] = defaultdict(list)
        self._errors: dict[str, list[datetime]] = defaultdict(list)
        self._successes: dict[str, list[datetime]] = defaultdict(list)
        self._failures: dict[str, list[datetime]] = defaultdict(list)

    def record_request(self, provider: str, latency_ms: float, success: bool):
        now = datetime.now(timezone.utc)
        cutoff = now - timedelta(minutes=self._window_minutes)
        self._latencies[provider].append(latency_ms)
        if success:
            self._successes[provider].append(now)
        else:
            self._errors[provider].append(now)
            self._failures[provider].append(now)
        self._trim(provider, cutoff)

    def _trim(self, provider: str, cutoff: datetime):
        self._latencies[provider] = self._latencies[provider][-10000:]
        self._errors[provider] = [t for t in self._errors[provider] if t > cutoff]
        self._successes[provider] = [t for t in self._successes[provider] if t > cutoff]
        self._failures[provider] = [t for t in self._failures[provider] if t > cutoff]

    def compute(self, provider: str) -> Optional[SLAMetrics]:
        latencies = self._latencies.get(provider, [])
        successes = self._successes.get(provider, [])
        errors = self._errors.get(provider, [])
        failures = self._failures.get(provider, [])
        total = len(successes) + len(errors)

        if total == 0:
            return None

        availability = len(successes) / total * 100 if total > 0 else 0.0
        error_rate = len(errors) / total if total > 0 else 0.0

        health = ProviderRegistry.get(provider)
        sla_target_avail = 99.5
        sla_target_p95 = 1000.0
        if health:
            sla_target_avail = getattr(health, "sla_target_availability", 99.5)
            sla_target_p95 = getattr(health, "sla_target_p95", 1000.0)

        p50 = statistics.median(latencies) if latencies else 0.0
        p95 = self._percentile(latencies, 95) if latencies else 0.0
        p99 = self._percentile(latencies, 99) if latencies else 0.0

        mtbf = self._compute_mtbf(failures) if len(failures) >= 2 else 0.0
        mttr = self._compute_mttr(failures) if failures else 0.0

        last_failure = max(failures) if failures else None
        last_success = max(successes) if successes else None

        now = datetime.now(timezone.utc)
        return SLAMetrics(
            provider=provider,
            availability=availability,
            uptime_ms=len(successes) * p50,
            total_requests=total,
            successful_requests=len(successes),
            failed_requests=len(errors),
            mttr_ms=mttr,
            mtbf_ms=mtbf,
            p50_ms=p50,
            p95_ms=p95,
            p99_ms=p99,
            error_rate=error_rate,
            last_failure=last_failure,
            last_success=last_success,
            period_start=now - timedelta(minutes=self._window_minutes),
            period_end=now,
            sla_target_availability=sla_target_avail,
            sla_target_p95=sla_target_p95,
        )

    def compute_all(self) -> dict[str, SLAMetrics]:
        results = {}
        for provider in list(self._latencies.keys()):
            metrics = self.compute(provider)
            if metrics:
                results[provider] = metrics
        return results

    def report(self) -> dict[str, dict]:
        return {
            p: m.to_dict()
            for p, m in self.compute_all().items()
        }

    @staticmethod
    def _percentile(data: list[float], p: int) -> float:
        if not data:
            return 0.0
        sorted_data = sorted(data)
        k = (len(sorted_data) - 1) * p / 100.0
        f = int(k)
        c = f + 1
        if c >= len(sorted_data):
            return sorted_data[-1]
        return sorted_data[f] + (k - f) * (sorted_data[c] - sorted_data[f])

    @staticmethod
    def _compute_mtbf(failures: list[datetime]) -> float:
        if len(failures) < 2:
            return 0.0
        sorted_f = sorted(failures)
        intervals = [(sorted_f[i + 1] - sorted_f[i]).total_seconds() * 1000 for i in range(len(sorted_f) - 1)]
        return statistics.mean(intervals) if intervals else 0.0

    @staticmethod
    def _compute_mttr(failures: list[datetime]) -> float:
        if len(failures) < 2:
            return 0.0
        sorted_f = sorted(failures)
        intervals = [(sorted_f[i + 1] - sorted_f[i]).total_seconds() * 1000 for i in range(len(sorted_f) - 1)]
        return statistics.mean(intervals) if intervals else 0.0
