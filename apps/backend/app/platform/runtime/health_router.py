from fastapi import APIRouter, Response

router = APIRouter()

try:
    from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
except Exception:  # pragma: no cover - optional dependency
    generate_latest = None
    CONTENT_TYPE_LATEST = "text/plain; version=0.0.4"

from apps.backend.app.modules.educacao.foundation.observability.health import (
    check_database,
    check_eventbus,
    check_redis,
)
from apps.backend.app.platform.integration.provider_registry import ProviderRegistry


@router.get("/api/health/live")
def api_health_live():
    return {"alive": True}


@router.get("/api/health")
def api_health():
    return {"status": "ok"}


@router.get("/api/health/ready")
async def api_health_ready():
    # run lightweight readiness checks in parallel
    import asyncio

    checks = await asyncio.gather(check_database(), check_redis(), check_eventbus())
    overall = all(c.healthy for c in checks)
    return {
        "ready": overall,
        "checks": {c.name: {"healthy": c.healthy, "details": c.details} for c in checks},
    }


@router.get("/api/health/providers")
def api_health_providers():
    return {
        "providers": ProviderRegistry.get_health_summary(),
        "summary": ProviderRegistry.get_status_summary(),
    }


@router.get("/system/health")
def system_health():
    return {"status": "ok", "system": "SILA"}


@router.get("/metrics")
def metrics():
    if not generate_latest:
        return Response(content="metrics not available", media_type="text/plain")
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)
