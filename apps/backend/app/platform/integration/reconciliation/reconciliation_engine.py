import logging
import time
from datetime import datetime, timezone
from typing import Any, Optional

from apps.backend.app.platform.integration.provider_registry import ProviderRegistry
from apps.backend.app.platform.integration.reconciliation.divergence_detector import (
    DivergenceDetector,
)
from apps.backend.app.platform.integration.reconciliation.reconciliation_report import (
    ReconciliationReport,
    ReconciliationStatus,
)

logger = logging.getLogger(__name__)


class ReconciliationEngine:
    def __init__(self):
        self._detector = DivergenceDetector()
        self._history: dict[str, ReconciliationReport] = {}

    async def reconcile(
        self,
        provider: str,
        fetch_internal_fn,
        fetch_provider_fn,
    ) -> ReconciliationReport:
        health = ProviderRegistry.get(provider)
        if not health:
            return ReconciliationReport(
                provider=provider,
                status=ReconciliationStatus.SKIPPED,
                error_message=f"Provider '{provider}' not registered",
            )
        if not health.enabled:
            return ReconciliationReport(
                provider=provider,
                status=ReconciliationStatus.SKIPPED,
                error_message=f"Provider '{provider}' is disabled",
            )

        start = time.monotonic()
        report = ReconciliationReport(provider=provider, status=ReconciliationStatus.OK)

        try:
            internal_data = await fetch_internal_fn()
            provider_data = await fetch_provider_fn()

            internal_refs = set(internal_data.get("refs", []))
            provider_refs = set(provider_data.get("refs", []))
            internal_amounts = internal_data.get("amounts", {})
            provider_amounts = provider_data.get("amounts", {})
            internal_statuses = internal_data.get("statuses", {})
            provider_statuses = provider_data.get("statuses", {})

            report.internal_count = len(internal_refs)
            report.provider_count = len(provider_refs)
            report.matched_count = len(internal_refs & provider_refs)
            report.total_amount_internal = sum(internal_amounts.values())
            report.total_amount_provider = sum(provider_amounts.values())

            divergences = self._detector.detect_all(
                internal_refs, provider_refs,
                internal_amounts, provider_amounts,
                internal_statuses, provider_statuses,
            )
            report.divergences = [d.to_dict() for d in divergences]
            if divergences:
                report.status = ReconciliationStatus.DIVERGENCE_FOUND

        except Exception as e:
            logger.error(f"reconciliation_error provider={provider} error={e}")
            report.status = ReconciliationStatus.FAILED
            report.error_message = str(e)

        report.completed_at = datetime.now(timezone.utc)
        report.duration_ms = (time.monotonic() - start) * 1000
        self._history[provider] = report
        return report

    def get_last_report(self, provider: str) -> Optional[ReconciliationReport]:
        return self._history.get(provider)

    def get_all_reports(self) -> dict[str, ReconciliationReport]:
        return dict(self._history)

    def clear(self) -> None:
        self._history.clear()
