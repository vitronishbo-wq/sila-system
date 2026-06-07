from __future__ import annotations

import logging
from typing import Optional
from uuid import UUID

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.educacao.domain.academic_identity import (
    AcademicIdentity,
    AcademicStatus,
    DuplicateResult,
    IdentityStatus,
)
from apps.backend.app.modules.educacao.infrastructure.models.academic_identity_model import (
    AcademicIdentityModel,
)
from apps.backend.app.modules.educacao.infrastructure.models.guardian_model import GuardianModel
from apps.backend.app.modules.educacao.infrastructure.models.guardian_student_link import (
    GuardianStudentLink,
)
from apps.backend.app.modules.educacao.infrastructure.models.identity_merge_model import (
    IdentityMergeModel,
)

logger = logging.getLogger(__name__)


class IdentityResolutionService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def resolve_by_bi(self, document_id: str) -> Optional[AcademicIdentity]:
        stmt = select(AcademicIdentityModel).where(
            AcademicIdentityModel.national_student_number == document_id
        )
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_entity(model) if model else None

    async def resolve_by_student_number(self, ns: str) -> Optional[AcademicIdentity]:
        stmt = select(AcademicIdentityModel).where(
            AcademicIdentityModel.national_student_number == ns
        )
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_entity(model) if model else None

    async def resolve_by_guardian(self, guardian_id: UUID) -> list[AcademicIdentity]:
        link_stmt = select(GuardianStudentLink.student_id).where(
            GuardianStudentLink.guardian_id == guardian_id
        )
        student_ids = (await self.session.execute(link_stmt)).scalars().all()
        if not student_ids:
            return []
        stmt = select(AcademicIdentityModel).where(
            AcademicIdentityModel.id.in_(student_ids)
        )
        models = (await self.session.execute(stmt)).scalars().all()
        return [self._to_entity(m) for m in models]

    async def find_duplicates(self) -> list[DuplicateResult]:
        results = []

        # Same BI/national_student_number (different IDs with same NS number)
        stmt = select(AcademicIdentityModel)
        models = (await self.session.execute(stmt)).scalars().all()

        seen: dict[str, list[AcademicIdentityModel]] = {}
        for m in models:
            seen.setdefault(m.national_student_number, []).append(m)

        for ns, group in seen.items():
            if len(group) > 1:
                primary = group[0]
                for dup in group[1:]:
                    results.append(DuplicateResult(
                        identity_id=dup.id,
                        duplicate_of=primary.id,
                        match_type="same_bi",
                        confidence="HIGH",
                        fields=["national_student_number"],
                    ))

        # Same name + birth_date
        name_dob: dict[tuple[str, str], list[AcademicIdentityModel]] = {}
        for m in models:
            key = (m.full_name.strip().lower(), str(m.birth_date))
            name_dob.setdefault(key, []).append(m)

        for key, group in name_dob.items():
            if len(group) > 1:
                primary = group[0]
                for dup in group[1:]:
                    dup_result = next(
                        (r for r in results if r.identity_id == dup.id), None
                    )
                    if not dup_result:
                        results.append(DuplicateResult(
                            identity_id=dup.id,
                            duplicate_of=primary.id,
                            match_type="same_name_birth",
                            confidence="MEDIUM",
                            fields=["full_name", "birth_date"],
                        ))

        # Same guardian + birth_date
        guardian_dob: dict[tuple[Optional[str], str], list[AcademicIdentityModel]] = {}
        for m in models:
            gid = str(m.guardian_id) if m.guardian_id else ""
            key = (gid, str(m.birth_date))
            guardian_dob.setdefault(key, []).append(m)

        for key, group in guardian_dob.items():
            if len(group) > 1 and key[0]:
                primary = group[0]
                for dup in group[1:]:
                    dup_result = next(
                        (r for r in results if r.identity_id == dup.id), None
                    )
                    if not dup_result:
                        results.append(DuplicateResult(
                            identity_id=dup.id,
                            duplicate_of=primary.id,
                            match_type="same_guardian_birth",
                            confidence="LOW",
                            fields=["guardian_id", "birth_date"],
                        ))

        return results

    async def mark_duplicate(self, identity_id: UUID) -> None:
        stmt = select(AcademicIdentityModel).where(AcademicIdentityModel.id == identity_id)
        model = (await self.session.execute(stmt)).scalars().first()
        if model:
            model.identity_status = IdentityStatus.SUSPECT_DUPLICATE.value
            await self.session.flush()

    async def create_merge_proposal(
        self, primary_id: UUID, duplicate_id: UUID, reason: str, confidence: str
    ) -> IdentityMergeModel:
        proposal = IdentityMergeModel(
            primary_identity_id=primary_id,
            duplicate_identity_id=duplicate_id,
            reason=reason,
            confidence=confidence,
            status="PENDING",
        )
        self.session.add(proposal)
        await self.session.flush()
        await self.session.refresh(proposal)
        return proposal

    async def list_merge_candidates(self, status: Optional[str] = None) -> list[IdentityMergeModel]:
        stmt = select(IdentityMergeModel).order_by(IdentityMergeModel.created_at.desc())
        if status:
            stmt = stmt.where(IdentityMergeModel.status == status)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    def _to_entity(self, m: AcademicIdentityModel) -> AcademicIdentity:
        return AcademicIdentity(
            id=m.id,
            national_student_number=m.national_student_number,
            full_name=m.full_name,
            birth_date=m.birth_date,
            gender=m.gender,
            nationality=m.nationality or "ANGOLANA",
            guardian_id=m.guardian_id,
            current_institution_id=m.current_institution_id,
            current_grade=m.current_grade,
            academic_status=AcademicStatus(m.academic_status) if m.academic_status else AcademicStatus.ACTIVE,
            identity_status=IdentityStatus(m.identity_status) if m.identity_status else IdentityStatus.VALID,
            created_at=m.created_at,
            updated_at=m.updated_at,
        )
