from __future__ import annotations

from uuid import UUID

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.educacao.application.ports import EnrollmentRepositoryPort
from apps.backend.app.modules.educacao.domain.models.enrollment import Enrollment, EnrollmentStatus
from apps.backend.app.modules.educacao.infrastructure.models.enrollment_model import EnrollmentModel


class SQLAlchemyEnrollmentRepository(EnrollmentRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, enrollment: Enrollment) -> Enrollment:
        model = await self.session.get(EnrollmentModel, enrollment.id)
        if not model:
            model = EnrollmentModel(id=enrollment.id)
            self.session.add(model)

        for key, value in enrollment.__dict__.items():
            if hasattr(model, key):
                setattr(model, key, value)
        
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, id: UUID) -> Enrollment | None:
        model = await self.session.get(EnrollmentModel, id)
        return self._to_domain(model) if model else None

    async def find_active_by_student_and_year(self, student_id: UUID, academic_year: str) -> Enrollment | None:
        stmt = select(EnrollmentModel).where(
            and_(
                EnrollmentModel.student_id == student_id,
                EnrollmentModel.academic_year == academic_year,
                EnrollmentModel.status.in_([EnrollmentStatus.ACTIVE, EnrollmentStatus.PENDING])
            )
        )
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    def _to_domain(self, model: EnrollmentModel) -> Enrollment:
        return Enrollment(**{key: getattr(model, key) for key in model.__table__.columns.keys()})
