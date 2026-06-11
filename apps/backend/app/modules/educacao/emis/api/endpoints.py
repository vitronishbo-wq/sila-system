"""EMIS Synchronization Admin Endpoints — trigger manual sync, monitor, reconcile."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.core.database.session import AsyncSessionLocal
from apps.backend.app.modules.educacao.emis.api.schemas import (
    SyncLogResponse,
    SyncStatsResponse,
)
from apps.backend.app.modules.educacao.emis.application.sync_engine import (
    EmisSyncEngine,
    SyncLogRepository,
)
from apps.backend.app.modules.educacao.emis.domain.models import SyncStatus
from apps.backend.app.modules.educacao.emis.infrastructure.sync_log_model import (
    EmisSyncLogModel,
)
from apps.backend.app.modules.educacao.infrastructure.models.enrollment_model import (
    EnrollmentModel,
)
from apps.backend.app.modules.educacao.infrastructure.models.escola_model import EscolaModel
from apps.backend.app.modules.educacao.infrastructure.models.academic_identity_model import AcademicIdentityModel
from apps.backend.app.api.deps import get_current_user
from apps.backend.app.core.rbac.territorial_access import verify_territorial_access

router = APIRouter(prefix="/emis", tags=["EMIS"])


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


async def _get_sync_engine(session: AsyncSession = Depends(get_db)):
    return EmisSyncEngine(session=session)


async def _get_log_repo(session: AsyncSession = Depends(get_db)):
    return SyncLogRepository(session)


@router.get("/health", response_model=dict)
async def emis_health():
    """Check EMIS external API connectivity."""
    try:
        from apps.backend.app.modules.educacao.emis.infrastructure.emis_client import EmisClient
        client = EmisClient()
        result = await client.health_check()
        return {"status": "connected", "response": result}
    except Exception as exc:
        return {"status": "unreachable", "error": str(exc)}


@router.post("/sync/enrollment/{enrollment_id}", response_model=dict)
async def sync_enrollment(
    enrollment_id: uuid.UUID,
    engine: EmisSyncEngine = Depends(_get_sync_engine),
    session: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """Push a single enrollment to EMIS."""
    try:
        # territorial check: ensure caller can act on the enrollment's institution
        enrollment = await session.get(EnrollmentModel, enrollment_id)
        if not enrollment:
            raise HTTPException(status_code=404, detail="Enrollment not found")
        escola = await session.get(EscolaModel, enrollment.institution_id)
        await verify_territorial_access(user=user, resource_territory_id=getattr(escola, "territory_id", None), db=session)
        result = await engine.push_enrollment(enrollment_id)
        return {"status": "success", "enrollment_id": str(enrollment_id), "result": result}
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"EMIS sync failed: {exc}")


@router.post("/sync/student/{student_id}", response_model=dict)
async def sync_student(
    student_id: uuid.UUID,
    engine: EmisSyncEngine = Depends(_get_sync_engine),
    session: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """Push a single student identity to EMIS."""
    try:
        # territorial check: based on student's current_institution_id when available
        student = await session.get(AcademicIdentityModel, student_id)
        if student and getattr(student, "current_institution_id", None):
            escola = await session.get(EscolaModel, student.current_institution_id)
            await verify_territorial_access(user=user, resource_territory_id=getattr(escola, "territory_id", None), db=session)
        result = await engine.push_student(student_id)
        return {"status": "success", "student_id": str(student_id), "result": result}
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"EMIS sync failed: {exc}")


@router.post("/sync/institution/{institution_id}", response_model=dict)
async def sync_institution(
    institution_id: uuid.UUID,
    engine: EmisSyncEngine = Depends(_get_sync_engine),
    session: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """Push a single institution to EMIS."""
    try:
        escola = await session.get(EscolaModel, institution_id)
        await verify_territorial_access(user=user, resource_territory_id=getattr(escola, "territory_id", None), db=session)
        result = await engine.push_institution(institution_id)
        return {"status": "success", "institution_id": str(institution_id), "result": result}
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"EMIS sync failed: {exc}")


@router.post("/sync/bulk/enrollments", response_model=dict)
async def sync_all_enrollments(
    limit: int = Query(default=100, le=500),
    engine: EmisSyncEngine = Depends(_get_sync_engine),
):
    """Push all recent pending enrollments to EMIS."""
    result = await engine.sync_all_pending_enrollments(limit=limit)
    return {"status": "completed", **result}


@router.post("/sync/bulk/institutions", response_model=dict)
async def sync_all_institutions(
    limit: int = Query(default=100, le=500),
    engine: EmisSyncEngine = Depends(_get_sync_engine),
):
    """Push all institutions to EMIS."""
    result = await engine.sync_all_institutions(limit=limit)
    return {"status": "completed", **result}


@router.get("/logs", response_model=list[SyncLogResponse])
async def list_sync_logs(
    entity_type: str = Query(default=None),
    status: str = Query(default=None),
    limit: int = Query(default=50, le=200),
    offset: int = Query(default=0, ge=0),
    repo: SyncLogRepository = Depends(_get_log_repo),
):
    """List EMIS sync logs with optional filters."""
    models = await repo.list_logs(
        entity_type=entity_type, status=status, limit=limit, offset=offset
    )
    return [
        SyncLogResponse(
            id=m.id,
            entity_type=m.entity_type,
            entity_id=m.entity_id,
            direction=m.direction,
            status=m.status,
            payload=m.payload,
            response=m.response,
            error=m.error,
            duration_ms=m.duration_ms,
            retry_count=m.retry_count,
            next_retry_at=m.next_retry_at,
            created_at=m.created_at,
        )
        for m in models
    ]


@router.get("/stats", response_model=SyncStatsResponse)
async def sync_stats(
    repo: SyncLogRepository = Depends(_get_log_repo),
):
    """EMIS Dashboard — total enviados, pendentes, falhados, reprocessados, última sincronização."""
    stats = await repo.get_stats()
    return SyncStatsResponse(**stats)


@router.post("/retry/dead-letter", response_model=dict)
async def retry_dead_letter(
    engine: EmisSyncEngine = Depends(_get_sync_engine),
    session: AsyncSession = Depends(get_db),
):
    """Reprocess all DEAD_LETTER and RETRY entries."""
    repo = SyncLogRepository(session)
    retryable = await repo.list_logs(
        status=SyncStatus.RETRY.value, limit=500
    )
    dead = await repo.list_logs(
        status=SyncStatus.DEAD_LETTER.value, limit=500
    )
    total = len(retryable) + len(dead)
    reprocessed = 0
    for entry in retryable + dead:
        try:
            if entry.entity_type == "enrollment":
                await engine.push_enrollment(uuid.UUID(entry.entity_id))
            elif entry.entity_type == "student":
                await engine.push_student(uuid.UUID(entry.entity_id))
            elif entry.entity_type == "institution":
                await engine.push_institution(uuid.UUID(entry.entity_id))
            reprocessed += 1
        except Exception:
            continue
    return {"reprocessed": reprocessed, "total": total}


@router.get("/reconciliation", response_model=dict)
async def reconciliation(
    session: AsyncSession = Depends(get_db),
    limit: int = Query(default=100, le=500),
):
    """Compare local enrollments vs EMIS sync status — produce divergences."""
    local_q = select(EnrollmentModel).order_by(EnrollmentModel.created_at.desc()).limit(limit)
    local_result = await session.execute(local_q)
    local = {str(m.id): m for m in local_result.scalars().all()}

    synced_q = (
        select(EmisSyncLogModel)
        .where(EmisSyncLogModel.entity_type == "enrollment")
        .order_by(EmisSyncLogModel.created_at.desc())
        .limit(limit * 2)
    )
    synced_result = await session.execute(synced_q)
    synced = {m.entity_id: m for m in synced_result.scalars().all()}

    never_synced = [eid for eid in local if eid not in synced]
    failed = [eid for eid, m in synced.items() if m.status in ("failed", "dead_letter") and eid in local]
    pending = [eid for eid, m in synced.items() if m.status == "pending" and eid in local]
    ok = [eid for eid, m in synced.items() if m.status == "success" and eid in local]

    return {
        "local_count": len(local),
        "synced_count": len(synced),
        "never_synced": never_synced[:20],
        "failed": failed[:20],
        "pending": pending[:20],
        "successfully_synced": len(ok),
        "divergence_pct": round((len(never_synced) + len(failed)) / max(len(local), 1) * 100, 1),
    }
