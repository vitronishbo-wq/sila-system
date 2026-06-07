from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import (
    SLABaseDB,
    SLAOverrideCreate,
    SLAOverrideDB,
    SLAPolicyCreate,
    SLAPolicyDB,
    SLAStatus,
    SLAVersionDB,
)


async def create_version_snapshot(
    db: AsyncSession,
    service_id: str,
    created_by: str | None = None,
    status: SLAStatus = SLAStatus.DRAFT,
) -> SLAVersionDB:
    base_result = await db.execute(select(SLABaseDB).where(SLABaseDB.service_id == service_id))
    base = base_result.scalar_one_or_none()
    if not base:
        raise ValueError(f"SLA base não encontrado: {service_id}")

    version = SLAVersionDB(
        version=base.version,
        service_id=service_id,
        base_hours=base.base_hours,
        changes=[],
        status=status.value,
        created_at=datetime.utcnow(),
    )
    db.add(version)
    await db.commit()
    await db.refresh(version)
    return version


async def approve_version(
    db: AsyncSession,
    version_id: str,
    approved_by: str | None = None,
) -> SLAVersionDB:
    version = await db.get(SLAVersionDB, version_id)
    if not version:
        raise ValueError("Versão não encontrada")
    version.status = SLAStatus.APPROVED.value
    version.approved_at = datetime.utcnow()
    version.approved_by = approved_by
    base_result = await db.execute(
        select(SLABaseDB).where(SLABaseDB.service_id == version.service_id)
    )
    base = base_result.scalar_one_or_none()
    if base:
        base.base_hours = version.base_hours
        base.version = version.version
    await db.commit()
    await db.refresh(version)
    return version


class SLAGovernance:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_policy(
        self, policy: SLAPolicyCreate, created_by: str | None = None
    ) -> SLAPolicyDB:
        record = SLAPolicyDB(
            scope=policy.scope,
            scope_id=policy.scope_id,
            service_id=policy.service_id,
            multiplier=policy.multiplier,
            min_hours=policy.min_hours,
            max_hours=policy.max_hours,
            enabled=True,
            reason=policy.reason,
            effective_from=policy.effective_from,
            effective_to=policy.effective_to,
            created_by=created_by,
            created_at=datetime.utcnow(),
        )
        self.db.add(record)
        await self.db.commit()
        await self.db.refresh(record)
        return record

    async def create_override(
        self, override: SLAOverrideCreate, created_by: str | None = None
    ) -> SLAOverrideDB:
        _ = created_by
        record = SLAOverrideDB(
            name=override.name,
            description=override.description,
            conditions=override.conditions,
            multiplier=override.multiplier,
            priority=override.priority,
            enabled=True,
            created_at=datetime.utcnow(),
        )
        self.db.add(record)
        await self.db.commit()
        await self.db.refresh(record)
        return record
