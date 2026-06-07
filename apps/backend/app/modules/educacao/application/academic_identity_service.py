from __future__ import annotations

import logging
from datetime import date
from typing import Any, Optional
from uuid import UUID

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.educacao.domain.academic_identity import (
    AcademicIdentity,
    AcademicStatus,
    DuplicateResult,
    GuardianRelationship,
    IdentityStatus,
)
from apps.backend.app.modules.educacao.infrastructure.models.academic_identity_model import (
    AcademicIdentityModel,
)
from apps.backend.app.modules.educacao.infrastructure.models.guardian_model import GuardianModel
from apps.backend.app.modules.educacao.infrastructure.models.guardian_student_link import (
    GuardianStudentLink,
)
from apps.backend.app.modules.educacao.application.student_number_generator import (
    StudentNumberGenerator,
)

logger = logging.getLogger(__name__)


class AcademicIdentityService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_identity(
        self,
        full_name: str,
        birth_date: date,
        gender: Optional[str] = None,
        nationality: str = "ANGOLANA",
        guardian_id: Optional[UUID] = None,
    ) -> AcademicIdentity:
        gen = StudentNumberGenerator(self.session)
        ns = await gen.generate()

        model = AcademicIdentityModel(
            national_student_number=ns,
            full_name=full_name,
            birth_date=birth_date,
            gender=gender,
            nationality=nationality,
            guardian_id=guardian_id,
            academic_status=AcademicStatus.ACTIVE.value,
            identity_status=IdentityStatus.VALID.value,
        )
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return self._model_to_entity(model)

    async def get_by_id(self, identity_id: UUID) -> Optional[AcademicIdentity]:
        model = await self.session.get(AcademicIdentityModel, identity_id)
        return self._model_to_entity(model) if model else None

    async def get_by_national_student_number(self, ns: str) -> Optional[AcademicIdentity]:
        stmt = select(AcademicIdentityModel).where(
            AcademicIdentityModel.national_student_number == ns
        )
        model = (await self.session.execute(stmt)).scalars().first()
        return self._model_to_entity(model) if model else None

    async def search_by_name(self, name: str, limit: int = 20) -> list[AcademicIdentity]:
        stmt = (
            select(AcademicIdentityModel)
            .where(AcademicIdentityModel.full_name.ilike(f"%{name}%"))
            .limit(limit)
        )
        models = (await self.session.execute(stmt)).scalars().all()
        return [self._model_to_entity(m) for m in models]

    async def search_by_document(self, document_id: str) -> list[AcademicIdentity]:
        stmt = select(AcademicIdentityModel).where(
            AcademicIdentityModel.national_student_number == document_id
        )
        model = (await self.session.execute(stmt)).scalars().first()
        if model:
            return [self._model_to_entity(model)]
        return []

    async def update_status(self, identity_id: UUID, status: AcademicStatus) -> Optional[AcademicIdentity]:
        model = await self.session.get(AcademicIdentityModel, identity_id)
        if not model:
            return None
        model.academic_status = status.value
        await self.session.flush()
        await self.session.refresh(model)
        return self._model_to_entity(model)

    async def list_all(self, limit: int = 100, offset: int = 0) -> list[AcademicIdentity]:
        stmt = (
            select(AcademicIdentityModel)
            .order_by(AcademicIdentityModel.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        models = (await self.session.execute(stmt)).scalars().all()
        return [self._model_to_entity(m) for m in models]

    async def count_by_status(self, status: AcademicStatus) -> int:
        stmt = (
            select(AcademicIdentityModel.id)
            .where(AcademicIdentityModel.academic_status == status.value)
        )
        result = await self.session.execute(stmt)
        return len(result.all())

    async def count_total(self) -> int:
        stmt = select(AcademicIdentityModel.id)
        result = await self.session.execute(stmt)
        return len(result.all())

    def _model_to_entity(self, m: AcademicIdentityModel) -> AcademicIdentity:
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
