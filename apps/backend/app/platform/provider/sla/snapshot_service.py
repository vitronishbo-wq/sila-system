import logging
from datetime import datetime, timedelta, timezone
from typing import Optional

from apps.backend.app.core.db import db
from apps.backend.app.platform.provider.sla.sla_engine import SLAEngine
from apps.backend.app.platform.provider.sla.snapshot import ProviderSLASnapshot
from sqlalchemy import select

logger = logging.getLogger(__name__)


class SLASnapshotService:
    def __init__(self, sla_engine: Optional[SLAEngine] = None):
        self._sla_engine = sla_engine or SLAEngine()

    async def take_snapshot(self, provider: str, measurement_mode: str = "simulated") -> Optional[ProviderSLASnapshot]:
        metrics = self._sla_engine.compute(provider)
        if not metrics:
            return None
        now = datetime.now(timezone.utc)
        async with db.session_factory() as session:
            snap = ProviderSLASnapshot(
                provider=provider,
                availability=metrics.availability,
                latency_p95=metrics.p95_ms,
                latency_p99=metrics.p99_ms,
                error_rate=metrics.error_rate,
                mttr=metrics.mttr_ms,
                mtbf=metrics.mtbf_ms,
                measurement_mode=measurement_mode,
                snapshot_timestamp=now,
            )
            session.add(snap)
            await session.commit()
            await session.refresh(snap)
            return snap

    async def take_all_snapshots(self) -> dict[str, ProviderSLASnapshot]:
        results = {}
        for provider in list(self._sla_engine._latencies.keys()):
            snap = await self.take_snapshot(provider)
            if snap:
                results[provider] = snap
        return results

    async def get_history(
        self,
        provider: str,
        hours: int = 24,
        limit: int = 100,
    ) -> list[ProviderSLASnapshot]:
        cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
        async with db.session_factory() as session:
            result = await session.execute(
                select(ProviderSLASnapshot).where(
                    ProviderSLASnapshot.provider == provider,
                    ProviderSLASnapshot.snapshot_timestamp >= cutoff,
                ).order_by(ProviderSLASnapshot.snapshot_timestamp.desc()).limit(limit)
            )
            return list(result.scalars().all())

    async def latest(self, provider: str) -> Optional[ProviderSLASnapshot]:
        async with db.session_factory() as session:
            result = await session.execute(
                select(ProviderSLASnapshot).where(
                    ProviderSLASnapshot.provider == provider
                ).order_by(ProviderSLASnapshot.snapshot_timestamp.desc()).limit(1)
            )
            return result.scalar_one_or_none()

    def to_dict(self, snap: ProviderSLASnapshot) -> dict:
        return {
            "provider": snap.provider,
            "availability": snap.availability,
            "latency_p95_ms": snap.latency_p95,
            "latency_p99_ms": snap.latency_p99,
            "error_rate": snap.error_rate,
            "mttr_ms": snap.mttr,
            "mtbf_ms": snap.mtbf,
            "measurement_mode": snap.measurement_mode,
            "snapshot_timestamp": snap.snapshot_timestamp.isoformat(),
        }
