from __future__ import annotations

import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.core.database.session import AsyncSessionLocal
from apps.backend.app.modules.educacao.api.schemas.academic_identity_schema import (
    AcademicIdentityCreate,
    AcademicIdentityResponse,
    AcademicIdentityUpdate,
    DuplicateResponse,
    GuardianCreate,
    GuardianLinkRequest,
    GuardianResponse,
    IdentityMetricsResponse,
    MergeCandidateResponse,
    MergeProposalCreate,
    MergeResolveRequest,
)
from apps.backend.app.modules.educacao.application.academic_identity_service import (
    AcademicIdentityService,
)
from apps.backend.app.modules.educacao.application.identity_governance_service import (
    IdentityGovernanceService,
)
from apps.backend.app.modules.educacao.application.identity_merge_service import (
    IdentityMergeService,
)
from apps.backend.app.modules.educacao.application.identity_resolution_service import (
    IdentityResolutionService,
)
from apps.backend.app.modules.educacao.domain.academic_identity import AcademicStatus
from apps.backend.app.modules.educacao.infrastructure.models import (
    AcademicIdentityModel,
    GuardianModel,
    GuardianStudentLink,
    IdentityMergeModel,
)

router = APIRouter(prefix="/students", tags=["Academic Identity"])


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@router.post("", response_model=AcademicIdentityResponse, status_code=201)
async def create_student(
    data: AcademicIdentityCreate,
    session: AsyncSession = Depends(get_db),
):
    svc = AcademicIdentityService(session)
    entity = await svc.create_identity(
        full_name=data.full_name,
        birth_date=data.birth_date,
        gender=data.gender,
        nationality=data.nationality,
        guardian_id=data.guardian_id,
    )
    await session.commit()
    return AcademicIdentityResponse(**entity.to_dict())


@router.get("/{identity_id}", response_model=AcademicIdentityResponse)
async def get_student(
    identity_id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
):
    svc = AcademicIdentityService(session)
    entity = await svc.get_by_id(identity_id)
    if not entity:
        raise HTTPException(404, detail="Student not found")
    return AcademicIdentityResponse(**entity.to_dict())


@router.get("", response_model=list[AcademicIdentityResponse])
async def list_students(
    limit: int = Query(100, le=500),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_db),
):
    svc = AcademicIdentityService(session)
    entities = await svc.list_all(limit=limit, offset=offset)
    return [AcademicIdentityResponse(**e.to_dict()) for e in entities]


@router.patch("/{identity_id}", response_model=AcademicIdentityResponse)
async def update_student(
    identity_id: uuid.UUID,
    data: AcademicIdentityUpdate,
    session: AsyncSession = Depends(get_db),
):
    svc = AcademicIdentityService(session)
    if data.academic_status:
        status_val = AcademicStatus(data.academic_status)
        entity = await svc.update_status(identity_id, status_val)
        if not entity:
            raise HTTPException(404, detail="Student not found")
        await session.commit()
        return AcademicIdentityResponse(**entity.to_dict())

    model = await session.get(AcademicIdentityModel, identity_id)
    if not model:
        raise HTTPException(404, detail="Student not found")
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if value is not None and hasattr(model, key):
            setattr(model, key, value)
    await session.flush()
    await session.refresh(model)
    entity = await svc.get_by_id(identity_id)
    return AcademicIdentityResponse(**entity.to_dict())


@router.get("/search/by-name", response_model=list[AcademicIdentityResponse])
async def search_students_by_name(
    q: str = Query(..., min_length=2),
    session: AsyncSession = Depends(get_db),
):
    svc = AcademicIdentityService(session)
    entities = await svc.search_by_name(q)
    return [AcademicIdentityResponse(**e.to_dict()) for e in entities]


@router.get("/search/by-ns", response_model=AcademicIdentityResponse)
async def search_student_by_ns(
    ns: str = Query(...),
    session: AsyncSession = Depends(get_db),
):
    svc = AcademicIdentityService(session)
    entity = await svc.get_by_national_student_number(ns)
    if not entity:
        raise HTTPException(404, detail="Student not found")
    return AcademicIdentityResponse(**entity.to_dict())


# ── Duplicate Detection ───────────────────────────────────

@router.get("/duplicates", response_model=list[DuplicateResponse])
async def detect_duplicates(
    session: AsyncSession = Depends(get_db),
):
    svc = IdentityResolutionService(session)
    results = await svc.find_duplicates()
    return [
        DuplicateResponse(
            identity_id=r.identity_id,
            duplicate_of=r.duplicate_of,
            match_type=r.match_type,
            confidence=r.confidence,
            fields=r.fields,
        )
        for r in results
    ]


@router.post("/{identity_id}/mark-duplicate", response_model=dict)
async def mark_as_duplicate(
    identity_id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
):
    svc = IdentityResolutionService(session)
    await svc.mark_duplicate(identity_id)
    await session.commit()
    return {"status": "marked", "identity_id": str(identity_id)}


# ── Merge Workflow ────────────────────────────────────────

@router.post("/merge/propose", response_model=MergeCandidateResponse)
async def propose_merge(
    data: MergeProposalCreate,
    session: AsyncSession = Depends(get_db),
):
    merge_svc = IdentityMergeService(session)
    gov_svc = IdentityGovernanceService(session)
    proposal = await merge_svc.open_merge(
        primary_identity_id=data.primary_identity_id,
        duplicate_identity_id=data.duplicate_identity_id,
        reason=data.reason,
        confidence=data.confidence,
        requested_by="api",
    )
    await gov_svc.governance_on_merge_requested(
        merge_id=str(proposal.id),
        primary_id=str(proposal.primary_identity_id),
        duplicate_id=str(proposal.duplicate_identity_id),
        confidence=proposal.confidence,
        reason=proposal.reason,
    )
    await session.commit()
    return MergeCandidateResponse(
        id=proposal.id,
        primary_identity_id=proposal.primary_identity_id,
        duplicate_identity_id=proposal.duplicate_identity_id,
        reason=proposal.reason,
        confidence=proposal.confidence,
        status=proposal.status,
        created_at=proposal.created_at,
    )


@router.get("/merge/pending", response_model=list[MergeCandidateResponse])
async def list_pending_merges(
    session: AsyncSession = Depends(get_db),
):
    merge_svc = IdentityMergeService(session)
    proposals = await merge_svc.list_merges(status="PENDING")
    return [
        MergeCandidateResponse(
            id=UUID(p["id"]),
            primary_identity_id=UUID(p["primary_identity_id"]),
            duplicate_identity_id=UUID(p["duplicate_identity_id"]),
            reason=p["reason"],
            confidence=p["confidence"],
            status=p["status"],
            resolved_by=p.get("resolved_by"),
            created_at=p.get("created_at"),
            resolved_at=p.get("resolved_at"),
        )
        for p in proposals
    ]


@router.post("/merge/{merge_id}/approve", response_model=dict)
async def approve_merge(
    merge_id: uuid.UUID,
    resolved_by: str = Query("api"),
    session: AsyncSession = Depends(get_db),
):
    merge_svc = IdentityMergeService(session)
    result = await merge_svc.approve_merge(merge_id, resolved_by)
    await session.commit()
    return result


@router.post("/merge/{merge_id}/execute", response_model=dict)
async def execute_merge(
    merge_id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
):
    merge_svc = IdentityMergeService(session)
    gov_svc = IdentityGovernanceService(session)
    result = await merge_svc.execute_merge(merge_id)
    await gov_svc.governance_on_merge_executed(
        merge_id=str(merge_id),
        primary_id=result["primary_identity_id"],
        duplicate_id=result["duplicate_identity_id"],
        merged_fields=result["merged_fields"],
    )
    await session.commit()
    return result


@router.post("/merge/{merge_id}/reject", response_model=dict)
async def reject_merge(
    merge_id: uuid.UUID,
    resolved_by: str = Query("api"),
    session: AsyncSession = Depends(get_db),
):
    merge_svc = IdentityMergeService(session)
    result = await merge_svc.reject_merge(merge_id, resolved_by)
    await session.commit()
    return result


@router.get("/merge/list", response_model=list[MergeCandidateResponse])
async def list_all_merges(
    status: str | None = Query(None),
    limit: int = Query(50, le=200),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_db),
):
    merge_svc = IdentityMergeService(session)
    proposals = await merge_svc.list_merges(status=status, limit=limit, offset=offset)
    return [
        MergeCandidateResponse(
            id=UUID(p["id"]),
            primary_identity_id=UUID(p["primary_identity_id"]),
            duplicate_identity_id=UUID(p["duplicate_identity_id"]),
            reason=p["reason"],
            confidence=p["confidence"],
            status=p["status"],
            resolved_by=p.get("resolved_by"),
            created_at=p.get("created_at"),
            resolved_at=p.get("resolved_at"),
        )
        for p in proposals
    ]


# ── Guardians ─────────────────────────────────────────────

@router.post("/guardians", response_model=GuardianResponse, status_code=201)
async def create_guardian(
    data: GuardianCreate,
    session: AsyncSession = Depends(get_db),
):
    model = GuardianModel(
        full_name=data.full_name,
        relationship=data.relationship,
        document_id=data.document_id,
        phone=data.phone,
        email=data.email,
        address=data.address,
        province=data.province,
        municipio=data.municipio,
    )
    session.add(model)
    await session.flush()
    await session.refresh(model)
    await session.commit()
    return GuardianResponse(
        id=model.id,
        full_name=model.full_name,
        relationship=model.relationship,
        document_id=model.document_id,
        phone=model.phone,
        email=model.email,
        address=model.address,
        province=model.province,
        municipio=model.municipio,
        created_at=model.created_at,
    )


@router.get("/guardians/{guardian_id}", response_model=GuardianResponse)
async def get_guardian(
    guardian_id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
):
    model = await session.get(GuardianModel, guardian_id)
    if not model:
        raise HTTPException(404, detail="Guardian not found")
    return GuardianResponse(
        id=model.id,
        full_name=model.full_name,
        relationship=model.relationship,
        document_id=model.document_id,
        phone=model.phone,
        email=model.email,
        address=model.address,
        province=model.province,
        municipio=model.municipio,
        created_at=model.created_at,
    )


@router.post("/guardians/link", response_model=dict)
async def link_guardian(
    data: GuardianLinkRequest,
    session: AsyncSession = Depends(get_db),
):
    existing = await session.get(GuardianModel, data.guardian_id)
    if not existing:
        raise HTTPException(404, detail="Guardian not found")
    check = (await session.execute(
        select(GuardianStudentLink).where(
            GuardianStudentLink.guardian_id == data.guardian_id,
            GuardianStudentLink.student_id == data.student_id,
        )
    )).scalars().first()
    if check:
        return {"status": "already_linked"}
    link = GuardianStudentLink(
        guardian_id=data.guardian_id,
        student_id=data.student_id,
        relationship=data.relationship,
    )
    session.add(link)
    await session.commit()
    return {"status": "linked"}


@router.get("/{identity_id}/guardians", response_model=list[GuardianResponse])
async def list_student_guardians(
    identity_id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
):
    links = (await session.execute(
        select(GuardianStudentLink).where(GuardianStudentLink.student_id == identity_id)
    )).scalars().all()
    guardians = []
    for link in links:
        g = await session.get(GuardianModel, link.guardian_id)
        if g:
            guardians.append(GuardianResponse(
                id=g.id,
                full_name=g.full_name,
                relationship=link.relationship,
                document_id=g.document_id,
                phone=g.phone,
                email=g.email,
                address=g.address,
                province=g.province,
                municipio=g.municipio,
                created_at=g.created_at,
            ))
    return guardians


# ── Identity Metrics ──────────────────────────────────────

@router.get("/metrics/identity", response_model=IdentityMetricsResponse)
async def identity_metrics(
    session: AsyncSession = Depends(get_db),
):
    svc = AcademicIdentityService(session)
    res = IdentityResolutionService(session)

    total = await svc.count_total()
    active = await svc.count_by_status(AcademicStatus.ACTIVE)
    graduated = await svc.count_by_status(AcademicStatus.GRADUATED)
    duplicates = len(await res.find_duplicates())
    merges = len(await res.list_merge_candidates(status="PENDING"))

    return IdentityMetricsResponse(
        total_identities=total,
        active_count=active,
        graduated_count=graduated,
        duplicates_found=duplicates,
        pending_merges=merges,
    )


# ── Identity Dashboard ────────────────────────────────────

@router.get("/dashboard", response_model=dict)
async def identity_dashboard(
    session: AsyncSession = Depends(get_db),
):
    from datetime import datetime, timedelta, timezone

    from apps.backend.app.modules.educacao.infrastructure.models import StudentNumberCounter

    svc = AcademicIdentityService(session)
    res = IdentityResolutionService(session)
    merge_svc = IdentityMergeService(session)

    total = await svc.count_total()
    active = await svc.count_by_status(AcademicStatus.ACTIVE)
    graduated = await svc.count_by_status(AcademicStatus.GRADUATED)
    transferred = await svc.count_by_status(AcademicStatus.TRANSFERRED)
    duplicates_found = len(await res.find_duplicates())
    pending_merges = len(await res.list_merge_candidates(status="PENDING"))
    approved_merges = len(await merge_svc.list_merges(status="APPROVED"))
    executed_merges = len(await merge_svc.list_merges(status="EXECUTED"))

    counters = (await session.execute(
        select(StudentNumberCounter)
    )).scalars().all()
    total_ens = sum(c.last_sequence for c in counters)

    now = datetime.now(timezone.utc)
    thirty_days_ago = now - timedelta(days=30)
    from apps.backend.app.modules.educacao.infrastructure.models import AcademicIdentityModel
    new_identities = (await session.execute(
        select(AcademicIdentityModel).where(
            AcademicIdentityModel.created_at >= thirty_days_ago
        )
    )).scalars().all()

    return {
        "identidades": total,
        "ativas": active,
        "graduadas": graduated,
        "transferidas": transferred,
        "duplicados": duplicates_found,
        "fusoes_pendentes": pending_merges,
        "fusoes_aprovadas": approved_merges,
        "fusoes_executadas": executed_merges,
        "novas_identidades_30d": len(new_identities),
        "ens_emitidos": total_ens,
        "taxa_duplicacao_pct": round(duplicates_found / total * 100, 2) if total > 0 else 0,
    }
