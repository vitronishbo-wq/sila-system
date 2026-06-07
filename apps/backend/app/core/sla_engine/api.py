from __future__ import annotations

import os
from datetime import datetime, timedelta
from typing import Any

from apps.backend.app.api.deps import get_current_user, get_db
from apps.backend.app.core.observability import trace
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .cache import SLACache
from .calculator import SLACalculator
from .events import SLAEventEmitter, emit_sla_calculated
from .governance import SLAGovernance
from .metrics import SLAMetrics
from .models import (
    CitizenType,
    Province,
    SLABaseDB,
    SLAContext,
    SLAOverrideCreate,
    SLAPolicyCreate,
    SLAPredictRequest,
    SLARequest,
    SLAResponse,
    SLAViolationDB,
    SLAViolationResponse,
)

try:
    import redis.asyncio as redis_async
except Exception:
    redis_async = None

router = APIRouter(prefix="/sla", tags=["SLA Engine"])
current_user_dep = Depends(get_current_user)
db_dep = Depends(get_db)
province_query = Query(Province.LUANDA)
citizen_type_query = Query(CitizenType.NORMAL)
days_query = Query(7, ge=1, le=90)

_REDIS_URL = os.getenv("SLA_REDIS_URL") or os.getenv("REDIS_URL")
_REDIS = (
    redis_async.from_url(_REDIS_URL, decode_responses=True) if redis_async and _REDIS_URL else None
)


def _cache() -> SLACache | None:
    return SLACache(_REDIS) if _REDIS else None


@router.post("/calculate", response_model=SLAResponse)
@trace("sla_calculate")
async def calculate_sla(
    request: SLARequest,
    db: AsyncSession = db_dep,
    current_user: dict[str, Any] = current_user_dep,
) -> SLAResponse:
    calculator = SLACalculator(db, cache=_cache())
    try:
        result = await calculator.calculate(request.service_id, request.context)
        emit_sla_calculated(
            {
                "service_id": result.service_id,
                "calculated_hours": result.calculated_hours,
                "user_id": current_user.get("id"),
            }
        )
        return result
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro no cálculo: {str(exc)}") from exc


@router.post("/calculate/batch", response_model=list[SLAResponse | None])
async def calculate_batch_sla(
    requests: list[SLARequest],
    background_tasks: BackgroundTasks,
    db: AsyncSession = db_dep,
) -> list[SLAResponse | None]:
    calculator = SLACalculator(db, cache=_cache(), metrics=SLAMetrics())
    batch_requests = [(req.service_id, req.context) for req in requests]
    results = await calculator.calculate_batch(batch_requests)
    background_tasks.add_task(lambda: calculator.metrics.record_batch_calculation(len(requests)))
    return results


@router.post("/predict")
async def predict_sla_breach(
    payload: SLAPredictRequest,
    db: AsyncSession = db_dep,
) -> dict[str, Any]:
    calculator = SLACalculator(db, cache=_cache())
    return await calculator.predict_breach(
        payload.service_id,
        payload.elapsed_hours,
        payload.context,
    )


@router.get("/service/{service_id}")
async def get_service_sla(
    service_id: str,
    province: Province = province_query,
    citizen_type: CitizenType = citizen_type_query,
    db: AsyncSession = db_dep,
) -> SLAResponse:
    context = SLAContext(province=province, citizen_type=citizen_type)
    calculator = SLACalculator(db, cache=_cache())
    return await calculator.calculate(service_id, context)


@router.post("/policies")
async def create_policy(
    policy: SLAPolicyCreate,
    db: AsyncSession = db_dep,
    current_user: dict[str, Any] = current_user_dep,
) -> dict[str, Any]:
    governance = SLAGovernance(db)
    record = await governance.create_policy(policy=policy, created_by=current_user.get("email"))
    SLAEventEmitter().policy_created(policy.model_dump())
    return {"id": record.id}


@router.post("/overrides")
async def create_override(
    override: SLAOverrideCreate,
    db: AsyncSession = db_dep,
    current_user: dict[str, Any] = current_user_dep,
) -> dict[str, Any]:
    governance = SLAGovernance(db)
    record = await governance.create_override(
        override=override, created_by=current_user.get("email")
    )
    SLAEventEmitter().override_created(override.model_dump())
    return {"id": record.id}


@router.get("/violations", response_model=list[SLAViolationResponse])
async def get_violations(
    service_id: str | None = None,
    province: Province | None = None,
    days: int = days_query,
    db: AsyncSession = db_dep,
) -> list[SLAViolationResponse]:
    since = datetime.utcnow() - timedelta(days=days)
    stmt = (
        select(SLAViolationDB, SLABaseDB.service_name)
        .outerjoin(SLABaseDB, SLABaseDB.service_id == SLAViolationDB.service_id)
        .where(SLAViolationDB.created_at >= since)
    )
    if service_id:
        stmt = stmt.where(SLAViolationDB.service_id == service_id)
    if province:
        stmt = stmt.where(SLAViolationDB.province == province.value)
    result = await db.execute(stmt.order_by(SLAViolationDB.created_at.desc()).limit(100))
    violations = result.all()
    responses: list[SLAViolationResponse] = []
    for v, service_name in violations:
        breach_pct = round((v.actual_hours / v.target_hours) * 100, 2) if v.target_hours else 0
        severity = "high" if v.delta_hours > (v.target_hours or 0) * 0.5 else "medium"
        responses.append(
            SLAViolationResponse(
                id=v.id,
                request_id=v.request_id,
                service_id=v.service_id,
                service_name=service_name or "",
                target_hours=v.target_hours,
                actual_hours=v.actual_hours,
                delta_hours=v.delta_hours,
                breach_percentage=breach_pct,
                severity=severity,
                province=v.province,
                citizen_type=v.citizen_type,
                escalated=v.escalated,
                created_at=v.created_at,
            )
        )
    return responses


@router.post("/violations/{violation_id}/escalate")
async def escalate_violation(
    violation_id: str,
    db: AsyncSession = db_dep,
    current_user: dict[str, Any] = current_user_dep,
) -> dict[str, Any]:
    _ = current_user
    violation = await db.get(SLAViolationDB, violation_id)
    if not violation:
        raise HTTPException(status_code=404, detail="Violação não encontrada")
    violation.escalated = True
    violation.escalation_level += 1
    await db.commit()
    SLAEventEmitter().violation_escalated(violation_id, violation.escalation_level)
    return {"status": "escalated", "level": violation.escalation_level}


@router.get("/health")
async def sla_health_check(db: AsyncSession = db_dep) -> dict[str, Any]:
    try:
        result = await db.execute(select(SLABaseDB))
        count = len(result.scalars().all())
        return {
            "status": "healthy",
            "services_count": count,
            "version": "2.0.0",
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as exc:
        raise HTTPException(
            status_code=503, detail={"status": "unhealthy", "error": str(exc)}
        ) from exc


@router.get("/base/{service_id}")
async def get_base_sla(
    service_id: str,
    db: AsyncSession = db_dep,
) -> dict[str, Any]:
    result = await db.execute(select(SLABaseDB).where(SLABaseDB.service_id == service_id))
    base = result.scalar_one_or_none()
    if not base:
        raise HTTPException(status_code=404, detail="SLA base não encontrado")
    return {
        "service_id": base.service_id,
        "service_name": base.service_name,
        "module": base.module,
        "base_hours": base.base_hours,
        "priority": base.priority,
        "tier": base.tier,
        "version": base.version,
        "legal_basis": base.legal_basis,
    }


@router.get("/base")
async def list_base_sla(db: AsyncSession = db_dep) -> list[dict[str, Any]]:
    result = await db.execute(
        select(SLABaseDB).order_by(SLABaseDB.module.asc(), SLABaseDB.service_name.asc())
    )
    rows = result.scalars().all()
    return [
        {
            "service_id": row.service_id,
            "service_name": row.service_name,
            "module": row.module,
            "base_hours": row.base_hours,
            "priority": row.priority,
            "tier": row.tier,
            "version": row.version,
        }
        for row in rows
    ]
