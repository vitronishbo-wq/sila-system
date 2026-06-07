import asyncio
import logging
from datetime import datetime, timezone
from typing import Any, Optional

from apps.backend.app.platform.integration.provider_registry import ProviderRegistry
from apps.backend.app.platform.integration.reconciliation.reconciliation_engine import (
    ReconciliationEngine,
)
from apps.backend.app.platform.integration.reconciliation.reconciliation_report import (
    ReconciliationStatus,
)

logger = logging.getLogger(__name__)


class ReconciliationJob:
    def __init__(self, engine: Optional[ReconciliationEngine] = None):
        self._engine = engine or ReconciliationEngine()
        self._running = False
        self._task: Optional[asyncio.Task] = None

    @property
    def engine(self) -> ReconciliationEngine:
        return self._engine

    async def run_all(self, providers: Optional[list[str]] = None) -> dict[str, dict]:
        results = {}
        targets = providers or list(ProviderRegistry.list_registered().keys())
        for provider in targets:
            health = ProviderRegistry.get(provider)
            if not health or not health.enabled:
                results[provider] = {"status": "skipped", "reason": "disabled"}
                continue
            p = provider
            report = await self._engine.reconcile(
                provider=provider,
                fetch_internal_fn=lambda p=p: self._default_internal_fetch(p),
                fetch_provider_fn=lambda p=p: self._default_provider_fetch(p),
            )
            results[provider] = report.to_dict()
        return results

    async def run_single(self, provider: str) -> dict:
        p = provider
        report = await self._engine.reconcile(
            provider=provider,
            fetch_internal_fn=lambda p=p: self._default_internal_fetch(p),
            fetch_provider_fn=lambda p=p: self._default_provider_fetch(p),
        )
        return report.to_dict()

    async def _default_internal_fetch(self, provider: str) -> dict:
        return {"refs": [], "amounts": {}, "statuses": {}}

    async def _default_provider_fetch(self, provider: str) -> dict:
        return {"refs": [], "amounts": {}, "statuses": {}}

    async def start_scheduler(self, interval_hours: int = 24):
        if self._running:
            logger.warning("reconciliation_scheduler already running")
            return
        self._running = True
        self._task = asyncio.create_task(self._run_periodic(interval_hours))
        logger.info(f"reconciliation_scheduler started interval={interval_hours}h")

    async def stop_scheduler(self):
        self._running = False
        if self._task:
            self._task.cancel()
            self._task = None
        logger.info("reconciliation_scheduler stopped")

    async def _run_periodic(self, interval_hours: int):
        while self._running:
            logger.info("reconciliation_scheduler starting cycle")
            await self.run_all()
            logger.info(f"reconciliation_scheduler sleeping {interval_hours}h")
            await asyncio.sleep(interval_hours * 3600)
