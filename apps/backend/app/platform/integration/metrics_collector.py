import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

from apps.backend.app.platform.integration.provider_registry import ProviderRegistry

logger = logging.getLogger(__name__)


@dataclass
class ProviderMetricsSnapshot:
    provider: str
    timestamp: datetime
    success_count: int
    error_count: int
    availability: float
    latency_p50: float
    latency_p95: float
    latency_p99: float


class MetricsCollector:
    _history: list[ProviderMetricsSnapshot] = []
    _max_history: int = 10000

    @classmethod
    def snapshot(cls, provider: str) -> Optional[ProviderMetricsSnapshot]:
        health = ProviderRegistry.get(provider)
        if not health:
            return None
        snapshot = ProviderMetricsSnapshot(
            provider=provider,
            timestamp=datetime.now(timezone.utc),
            success_count=health.metrics.success_count,
            error_count=health.metrics.error_count,
            availability=health.metrics.availability,
            latency_p50=health.metrics.latency_p50,
            latency_p95=health.metrics.latency_p95,
            latency_p99=health.metrics.latency_p99,
        )
        cls._history.append(snapshot)
        if len(cls._history) > cls._max_history:
            cls._history.pop(0)
        return snapshot

    @classmethod
    def snapshot_all(cls) -> list[ProviderMetricsSnapshot]:
        results = []
        for provider in ProviderRegistry.list_registered():
            snap = cls.snapshot(provider)
            if snap:
                results.append(snap)
        return results

    @classmethod
    def get_history(
        cls, provider: str, limit: int = 100
    ) -> list[ProviderMetricsSnapshot]:
        return [s for s in cls._history if s.provider == provider][-limit:]

    @classmethod
    def clear(cls) -> None:
        cls._history.clear()

    @classmethod
    def report(cls) -> dict:
        return {
            provider: {
                "availability": h.metrics.availability,
                "success_rate": h.metrics.success_rate,
                "error_rate": h.metrics.error_rate,
                "p50": h.metrics.latency_p50,
                "p95": h.metrics.latency_p95,
                "p99": h.metrics.latency_p99,
                "success_count": h.metrics.success_count,
                "error_count": h.metrics.error_count,
                "last_success": h.metrics.last_success.isoformat() if h.metrics.last_success else None,
                "last_error": h.metrics.last_error.isoformat() if h.metrics.last_error else None,
                "last_error_message": h.metrics.last_error_message,
            }
            for provider, h in ProviderRegistry.list_registered().items()
        }


__all__ = ["MetricsCollector"]
