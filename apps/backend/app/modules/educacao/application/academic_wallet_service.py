from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.educacao.infrastructure.models.academic_identity_model import (
    AcademicIdentityModel,
)
from apps.backend.app.modules.educacao.infrastructure.models.academic_record_model import (
    AcademicRecordModel,
)
from apps.backend.app.modules.educacao.infrastructure.models.enrollment_model import EnrollmentModel
from apps.backend.app.modules.educacao.infrastructure.models.guardian_model import GuardianModel
from apps.backend.app.modules.educacao.infrastructure.models.guardian_student_link import (
    GuardianStudentLink,
)


class AcademicWalletService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_wallet(self, identity_id: UUID) -> dict:
        identity = await self.session.get(AcademicIdentityModel, identity_id)
        if not identity:
            return {"error": "not_found"}

        record = (
            await self.session.execute(
                select(AcademicRecordModel).where(
                    AcademicRecordModel.academic_identity_id == identity_id
                )
            )
        ).scalars().first()

        enrollments = (
            await self.session.execute(
                select(EnrollmentModel).where(
                    EnrollmentModel.student_id == identity_id
                ).order_by(EnrollmentModel.created_at.desc())
            )
        ).scalars().all()

        links = (
            await self.session.execute(
                select(GuardianStudentLink).where(
                    GuardianStudentLink.student_id == identity_id
                )
            )
        ).scalars().all()

        guardians = []
        for link in links:
            g = await self.session.get(GuardianModel, link.guardian_id)
            if g:
                guardians.append({
                    "id": str(g.id),
                    "full_name": g.full_name,
                    "relationship": link.relationship,
                })

        active_enrollment = next(
            (e for e in enrollments if e.status == "ACTIVE"), None
        )

        return {
            "identity": {
                "id": str(identity.id),
                "national_student_number": identity.national_student_number,
                "full_name": identity.full_name,
                "academic_status": identity.academic_status,
                "identity_status": identity.identity_status,
            },
            "active_enrollment": {
                "id": str(active_enrollment.id) if active_enrollment else None,
                "institution_id": str(active_enrollment.institution_id) if active_enrollment else None,
                "academic_year": active_enrollment.academic_year if active_enrollment else None,
                "grade": active_enrollment.grade if active_enrollment else None,
            } if active_enrollment else None,
            "enrollment_history": [
                {
                    "id": str(e.id),
                    "institution_id": str(e.institution_id),
                    "academic_year": e.academic_year,
                    "grade": e.grade,
                    "status": e.status,
                    "started_at": e.started_at.isoformat() if e.started_at else None,
                    "ended_at": e.ended_at.isoformat() if e.ended_at else None,
                }
                for e in enrollments
            ],
            "record": {
                "completed_classes": record.completed_classes if record else [],
                "sanctions": record.sanctions if record else [],
            } if record else {"completed_classes": [], "sanctions": []},
            "guardians": guardians,
        }
