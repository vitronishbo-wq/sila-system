from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.educacao.domain.academic_identity import IdentityStatus
from apps.backend.app.modules.educacao.infrastructure.models import (
    AcademicIdentityModel,
    IdentityMergeModel,
)


class IdentityMergeService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.audit_trail: list[dict[str, Any]] = []

    async def open_merge(
        self,
        primary_identity_id: uuid.UUID,
        duplicate_identity_id: uuid.UUID,
        reason: str,
        confidence: str = "MEDIUM",
        requested_by: str | None = None,
    ) -> IdentityMergeModel:
        primary = await self.session.get(AcademicIdentityModel, primary_identity_id)
        if not primary:
            raise ValueError(f"Primary identity {primary_identity_id} not found")
        duplicate = await self.session.get(AcademicIdentityModel, duplicate_identity_id)
        if not duplicate:
            raise ValueError(f"Duplicate identity {duplicate_identity_id} not found")
        existing = await self._find_pending_merge(primary_identity_id, duplicate_identity_id)
        if existing:
            raise ValueError(f"Merge already exists between these identities (status={existing.status})")
        merge = IdentityMergeModel(
            id=uuid.uuid4(),
            primary_identity_id=primary_identity_id,
            duplicate_identity_id=duplicate_identity_id,
            reason=reason,
            confidence=confidence,
            status="PENDING",
            resolved_by=requested_by,
        )
        self.session.add(merge)
        await self.session.flush()
        self.audit_trail.append({
            "action": "merge_opened",
            "merge_id": str(merge.id),
            "primary": str(primary_identity_id),
            "duplicate": str(duplicate_identity_id),
            "reason": reason,
            "confidence": confidence,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        return merge

    async def approve_merge(
        self, merge_id: uuid.UUID, resolved_by: str
    ) -> dict[str, Any]:
        merge = await self.session.get(IdentityMergeModel, merge_id)
        if not merge:
            raise ValueError(f"Merge proposal {merge_id} not found")
        if merge.status != "PENDING":
            raise ValueError(f"Merge is not in PENDING state (current: {merge.status})")
        merge.status = "APPROVED"
        merge.resolved_by = resolved_by
        merge.resolved_at = datetime.now(timezone.utc)
        await self.session.flush()
        self.audit_trail.append({
            "action": "merge_approved",
            "merge_id": str(merge_id),
            "resolved_by": resolved_by,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        return {
            "merge_id": str(merge.id),
            "status": merge.status,
            "primary_identity_id": str(merge.primary_identity_id),
            "duplicate_identity_id": str(merge.duplicate_identity_id),
            "resolved_by": resolved_by,
            "resolved_at": merge.resolved_at.isoformat() if merge.resolved_at else None,
        }

    async def execute_merge(self, merge_id: uuid.UUID) -> dict[str, Any]:
        merge = await self.session.get(IdentityMergeModel, merge_id)
        if not merge:
            raise ValueError(f"Merge proposal {merge_id} not found")
        if merge.status != "APPROVED":
            raise ValueError(f"Cannot execute merge: status is {merge.status}, expected APPROVED")

        primary_id = merge.primary_identity_id
        duplicate_id = merge.duplicate_identity_id

        primary = await self.session.get(AcademicIdentityModel, primary_id)
        duplicate = await self.session.get(AcademicIdentityModel, duplicate_id)
        if not primary or not duplicate:
            raise ValueError("One or both identities not found")

        merged_fields: dict[str, Any] = {}
        if not primary.full_name and duplicate.full_name:
            merged_fields["full_name"] = duplicate.full_name
        if duplicate.nationality and duplicate.nationality != "ANGOLANA" and (not primary.nationality or primary.nationality == "ANGOLANA"):
            merged_fields["nationality"] = duplicate.nationality
        if not primary.guardian_id and duplicate.guardian_id:
            merged_fields["guardian_id"] = duplicate.guardian_id
        if not primary.current_institution_id and duplicate.current_institution_id:
            merged_fields["current_institution_id"] = duplicate.current_institution_id
        if not primary.current_grade and duplicate.current_grade:
            merged_fields["current_grade"] = duplicate.current_grade

        if merged_fields:
            stmt = (
                update(AcademicIdentityModel)
                .where(AcademicIdentityModel.id == primary_id)
                .values(**merged_fields)
            )
            await self.session.execute(stmt)

        stmt_dup = (
            update(AcademicIdentityModel)
            .where(AcademicIdentityModel.id == duplicate_id)
            .values(identity_status=IdentityStatus.MERGED.value)
        )
        await self.session.execute(stmt_dup)

        merge.status = "EXECUTED"
        merge.resolved_at = datetime.now(timezone.utc)
        await self.session.flush()

        self.audit_trail.append({
            "action": "merge_executed",
            "merge_id": str(merge_id),
            "primary_id": str(primary_id),
            "duplicate_id": str(duplicate_id),
            "merged_fields": list(merged_fields.keys()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

        return {
            "merge_id": str(merge.id),
            "status": merge.status,
            "primary_identity_id": str(primary_id),
            "duplicate_identity_id": str(duplicate_id),
            "merged_fields": list(merged_fields.keys()),
            "duplicate_marked_as": IdentityStatus.MERGED.value,
        }

    async def reject_merge(
        self, merge_id: uuid.UUID, resolved_by: str, reason: str | None = None
    ) -> dict[str, Any]:
        merge = await self.session.get(IdentityMergeModel, merge_id)
        if not merge:
            raise ValueError(f"Merge proposal {merge_id} not found")
        merge.status = "REJECTED"
        merge.resolved_by = resolved_by
        merge.resolved_at = datetime.now(timezone.utc)
        await self.session.flush()
        self.audit_trail.append({
            "action": "merge_rejected",
            "merge_id": str(merge_id),
            "resolved_by": resolved_by,
            "reason": reason,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        return {
            "merge_id": str(merge.id),
            "status": merge.status,
        }

    async def _find_pending_merge(
        self, primary_id: uuid.UUID, duplicate_id: uuid.UUID
    ) -> IdentityMergeModel | None:
        stmt = select(IdentityMergeModel).where(
            IdentityMergeModel.primary_identity_id == primary_id,
            IdentityMergeModel.duplicate_identity_id == duplicate_id,
            IdentityMergeModel.status.in_(["PENDING", "APPROVED"]),
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def list_merges(
        self, status: str | None = None, limit: int = 50, offset: int = 0
    ) -> list[dict[str, Any]]:
        stmt = select(IdentityMergeModel).order_by(IdentityMergeModel.created_at.desc())
        if status:
            stmt = stmt.where(IdentityMergeModel.status == status)
        stmt = stmt.offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        merges = result.scalars().all()
        return [
            {
                "id": str(m.id),
                "primary_identity_id": str(m.primary_identity_id),
                "duplicate_identity_id": str(m.duplicate_identity_id),
                "reason": m.reason,
                "confidence": m.confidence,
                "status": m.status,
                "resolved_by": m.resolved_by,
                "created_at": m.created_at.isoformat() if m.created_at else None,
                "resolved_at": m.resolved_at.isoformat() if m.resolved_at else None,
            }
            for m in merges
        ]
