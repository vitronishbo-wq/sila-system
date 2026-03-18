from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from .models import (
    SLABaseDB,
    SLAOverrideCreate,
    SLAOverrideDB,
    SLAPolicyCreate,
    SLAPolicyDB,
    SLAViolationDB,
    CitizenType,
    Province,
)

router = APIRouter(prefix="/admin/sla", tags=["SLA Admin"])
templates = Jinja2Templates(directory="templates")


def _assert_admin(current_user: dict[str, Any]) -> None:
    role = (current_user.get("role") or "").upper()
    if not role or role == "CITIZEN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")


@router.post("/base", status_code=201)
async def create_base_sla(
    payload: dict[str, Any],
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    _assert_admin(current_user)
    record = SLABaseDB(
        service_id=payload["service_id"],
        service_name=payload["service_name"],
        service_description=payload.get("service_description"),
        module=payload.get("module", "general"),
        base_hours=float(payload["base_hours"]),
        priority=payload.get("priority", "medium"),
        tier=payload.get("tier", "silver"),
        legal_basis=payload.get("legal_basis"),
        version=payload.get("version", "1.0"),
        created_by=current_user.get("id"),
        metadata_json=payload.get("metadata") or {},
    )
    db.add(record)
    await db.commit()
    await db.refresh(record)
    return {"id": record.id, "service_id": record.service_id}


@router.get("/policies")
async def list_policies(
    db: AsyncSession = Depends(get_db),
    current_user: dict[str, Any] = Depends(get_current_user),
) -> list[dict[str, Any]]:
    _assert_admin(current_user)
    result = await db.execute(select(SLAPolicyDB).order_by(SLAPolicyDB.created_at.desc()))
    rows = result.scalars().all()
    return [
        {
            "id": row.id,
            "scope": row.scope,
            "scope_id": row.scope_id,
            "service_id": row.service_id,
            "multiplier": row.multiplier,
            "min_hours": row.min_hours,
            "max_hours": row.max_hours,
            "enabled": row.enabled,
            "reason": row.reason,
        }
        for row in rows
    ]


@router.post("/policies", status_code=201)
async def create_policy(
    payload: SLAPolicyCreate,
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    _assert_admin(current_user)
    policy = SLAPolicyDB(
        scope=payload.scope,
        scope_id=payload.scope_id,
        service_id=payload.service_id,
        multiplier=payload.multiplier,
        min_hours=payload.min_hours,
        max_hours=payload.max_hours,
        enabled=True,
        reason=payload.reason,
        effective_from=payload.effective_from,
        effective_to=payload.effective_to,
        created_by=current_user.get("id"),
        created_at=datetime.utcnow(),
    )
    db.add(policy)
    await db.commit()
    await db.refresh(policy)
    return {"id": policy.id}


@router.post("/overrides", status_code=201)
async def create_override(
    payload: SLAOverrideCreate,
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    _assert_admin(current_user)
    override = SLAOverrideDB(
        name=payload.name,
        description=payload.description,
        conditions=payload.conditions,
        multiplier=payload.multiplier,
        priority=payload.priority,
        enabled=True,
        created_at=datetime.utcnow(),
    )
    db.add(override)
    await db.commit()
    await db.refresh(override)
    return {"id": override.id}


@router.get("/violations")
async def list_violations(
    db: AsyncSession = Depends(get_db),
    current_user: dict[str, Any] = Depends(get_current_user),
) -> list[dict[str, Any]]:
    _assert_admin(current_user)
    result = await db.execute(select(SLAViolationDB).order_by(SLAViolationDB.created_at.desc()))
    rows = result.scalars().all()
    return [
        {
            "id": row.id,
            "request_id": row.request_id,
            "service_id": row.service_id,
            "target_hours": row.target_hours,
            "actual_hours": row.actual_hours,
            "delta_hours": row.delta_hours,
            "province": row.province,
            "citizen_type": row.citizen_type,
            "escalated": row.escalated,
            "created_at": row.created_at,
        }
        for row in rows
    ]


@router.get("/dashboard", response_class=HTMLResponse)
async def sla_dashboard(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: dict[str, Any] = Depends(get_current_user),
) -> HTMLResponse:
    _assert_admin(current_user)
    total_services = await db.execute(select(func.count()).select_from(SLABaseDB))
    recent_violations = await db.execute(
        select(func.count()).select_from(SLAViolationDB).where(
            SLAViolationDB.created_at >= datetime.utcnow() - timedelta(days=7)
        )
    )
    top_violations = await db.execute(
        select(SLAViolationDB.service_id, func.count().label("count"))
        .group_by(SLAViolationDB.service_id)
        .order_by(func.count().desc())
        .limit(10)
    )
    by_module = await db.execute(
        select(SLABaseDB.module, func.count().label("count")).group_by(SLABaseDB.module)
    )
    return templates.TemplateResponse(
        "sla/dashboard.html",
        {
            "request": request,
            "user": current_user,
            "stats": {
                "total_services": total_services.scalar() or 0,
                "recent_violations": recent_violations.scalar() or 0,
                "top_violations": top_violations.all(),
                "by_module": dict(by_module.all()),
            },
        },
    )


@router.get("/simulator", response_class=HTMLResponse)
async def sla_simulator(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: dict[str, Any] = Depends(get_current_user),
) -> HTMLResponse:
    _assert_admin(current_user)
    services_result = await db.execute(select(SLABaseDB).limit(100))
    services = services_result.scalars().all()
    return templates.TemplateResponse(
        "sla/simulator.html",
        {
            "request": request,
            "user": current_user,
            "services": services,
            "provinces": Province.__members__.values(),
            "citizen_types": CitizenType.__members__.values(),
        },
    )
