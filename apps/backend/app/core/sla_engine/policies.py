from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List

from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import SLAContext, SLAOverrideDB, SLAPolicyDB


def _matches_condition(value: Any, expected: Any) -> bool:
    if isinstance(expected, (list, tuple, set)):
        return value in expected
    return value == expected


def _context_dict(context: SLAContext) -> dict[str, Any]:
    return {
        "province": context.province.value,
        "citizen_type": context.citizen_type.value,
        "channel": context.channel.value,
        "load_level": context.load_level.value,
        "is_holiday": context.is_holiday,
        "business_hours": context.business_hours,
    }


async def load_policies(
    db: AsyncSession,
    service_id: str,
    context: SLAContext,
) -> List[Dict[str, Any]]:
    now = datetime.utcnow()
    stmt = (
        select(SLAPolicyDB)
        .where(
            SLAPolicyDB.enabled.is_(True),
            SLAPolicyDB.effective_from <= now,
            or_(SLAPolicyDB.effective_to.is_(None), SLAPolicyDB.effective_to >= now),
            or_(SLAPolicyDB.service_id.is_(None), SLAPolicyDB.service_id == service_id),
        )
        .order_by(SLAPolicyDB.scope.asc())
    )
    result = await db.execute(stmt)
    rows = result.scalars().all()

    scoped: List[Dict[str, Any]] = []
    for row in rows:
        if row.scope == "global":
            scoped.append(_row_to_dict(row))
            continue
        if row.scope == "province" and row.scope_id == context.province.value:
            scoped.append(_row_to_dict(row))
            continue
        if row.scope == "channel" and row.scope_id == context.channel.value:
            scoped.append(_row_to_dict(row))
            continue
        if row.scope == "citizen_type" and row.scope_id == context.citizen_type.value:
            scoped.append(_row_to_dict(row))
            continue
    scoped.sort(key=lambda item: 0 if item.get("service_id") else 1)
    return scoped


async def load_overrides(
    db: AsyncSession,
    service_id: str,
    context: SLAContext,
) -> List[Dict[str, Any]]:
    stmt = (
        select(SLAOverrideDB)
        .where(SLAOverrideDB.enabled.is_(True))
        .order_by(SLAOverrideDB.priority.desc())
    )
    result = await db.execute(stmt)
    rows = result.scalars().all()
    ctx = _context_dict(context)
    overrides: List[Dict[str, Any]] = []
    for row in rows:
        conditions = row.conditions or {}
        if not conditions:
            continue
        if conditions.get("service_id") and conditions.get("service_id") != service_id:
            continue
        if all(_matches_condition(ctx.get(key), value) for key, value in conditions.items() if key in ctx):
            overrides.append(
                {
                    "id": row.id,
                    "name": row.name,
                    "description": row.description,
                    "multiplier": row.multiplier,
                    "priority": row.priority,
                    "conditions": conditions,
                }
            )
    return overrides


def _row_to_dict(row: SLAPolicyDB) -> Dict[str, Any]:
    return {
        "id": row.id,
        "scope": row.scope,
        "scope_id": row.scope_id,
        "service_id": row.service_id,
        "multiplier": row.multiplier,
        "max_hours": row.max_hours,
        "min_hours": row.min_hours,
        "reason": row.reason,
    }


class SLAPolicyManager:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list(self) -> List[Dict[str, Any]]:
        result = await self.db.execute(select(SLAPolicyDB))
        return [_row_to_dict(row) for row in result.scalars().all()]

    async def list_overrides(self) -> List[Dict[str, Any]]:
        result = await self.db.execute(select(SLAOverrideDB))
        rows = result.scalars().all()
        return [
            {
                "id": row.id,
                "name": row.name,
                "description": row.description,
                "conditions": row.conditions,
                "multiplier": row.multiplier,
                "priority": row.priority,
                "enabled": row.enabled,
            }
            for row in rows
        ]
