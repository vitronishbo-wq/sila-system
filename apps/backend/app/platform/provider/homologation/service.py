import hashlib
import json
import logging
from datetime import datetime, timezone
from typing import Optional

from apps.backend.app.core.db import db
from apps.backend.app.platform.provider.homologation.models import ProviderHomologationEvidence
from sqlalchemy import select

logger = logging.getLogger(__name__)


class HomologationEvidenceService:

    async def record(
        self,
        provider: str,
        endpoint: str,
        latency_ms: Optional[float] = None,
        status_code: Optional[int] = None,
        auth_ok: bool = False,
        payload: Optional[dict] = None,
        operator: Optional[str] = None,
        result: str = "pending",
        details: Optional[str] = None,
    ) -> ProviderHomologationEvidence:
        payload_hash = None
        if payload:
            raw = json.dumps(payload, sort_keys=True)
            payload_hash = hashlib.sha256(raw.encode()).hexdigest()

        async with db.session_factory() as session:
            ev = ProviderHomologationEvidence(
                provider=provider,
                endpoint=endpoint,
                timestamp=datetime.now(timezone.utc),
                latency_ms=latency_ms,
                status_code=status_code,
                auth_ok=auth_ok,
                payload_hash=payload_hash,
                operator=operator,
                result=result,
                details=details,
            )
            session.add(ev)
            await session.commit()
            await session.refresh(ev)
            logger.info(
                "homologation_evidence provider=%s endpoint=%s result=%s latency=%.1fms",
                provider, endpoint, result, latency_ms or 0,
            )
            return ev

    async def list_by_provider(self, provider: str, limit: int = 50) -> list[ProviderHomologationEvidence]:
        async with db.session_factory() as session:
            result = await session.execute(
                select(ProviderHomologationEvidence)
                .where(ProviderHomologationEvidence.provider == provider)
                .order_by(ProviderHomologationEvidence.timestamp.desc())
                .limit(limit)
            )
            return list(result.scalars().all())

    async def list_all(self, limit: int = 100) -> list[ProviderHomologationEvidence]:
        async with db.session_factory() as session:
            result = await session.execute(
                select(ProviderHomologationEvidence)
                .order_by(ProviderHomologationEvidence.timestamp.desc())
                .limit(limit)
            )
            return list(result.scalars().all())

    async def summary(self) -> dict:
        rows = await self.list_all(limit=1000)
        summary: dict[str, dict] = {}
        for ev in rows:
            if ev.provider not in summary:
                summary[ev.provider] = {
                    "total": 0,
                    "passed": 0,
                    "failed": 0,
                    "last_timestamp": None,
                    "last_result": None,
                }
            s = summary[ev.provider]
            s["total"] += 1
            if ev.result == "passed":
                s["passed"] += 1
            else:
                s["failed"] += 1
            if s["last_timestamp"] is None or ev.timestamp > s["last_timestamp"]:
                s["last_timestamp"] = ev.timestamp.isoformat()
                s["last_result"] = ev.result
        return summary

    def to_dict(self, ev: ProviderHomologationEvidence) -> dict:
        return {
            "id": ev.id,
            "provider": ev.provider,
            "endpoint": ev.endpoint,
            "timestamp": ev.timestamp.isoformat(),
            "latency_ms": ev.latency_ms,
            "status_code": ev.status_code,
            "auth_ok": ev.auth_ok,
            "payload_hash": ev.payload_hash,
            "operator": ev.operator,
            "result": ev.result,
            "details": ev.details,
        }
