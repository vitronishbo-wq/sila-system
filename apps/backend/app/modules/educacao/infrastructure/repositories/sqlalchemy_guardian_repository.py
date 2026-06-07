from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.educacao.application.ports.guardian_repository_port import GuardianRepositoryPort
from apps.backend.app.modules.educacao.infrastructure.models.guardian_model import GuardianModel
from apps.backend.app.modules.educacao.infrastructure.models.guardian_student_link import GuardianStudentLink


class SQLAlchemyGuardianRepository(GuardianRepositoryPort):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, guardian: GuardianModel) -> GuardianModel:
        self._session.add(guardian)
        await self._session.flush()
        await self._session.refresh(guardian)
        return guardian

    async def get_by_id(self, guardian_id: UUID) -> GuardianModel | None:
        return await self._session.get(GuardianModel, guardian_id)

    async def find_by_document(self, document_id: str) -> list[GuardianModel]:
        stmt = select(GuardianModel).where(GuardianModel.document_id == document_id)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def find_by_student(self, student_id: UUID) -> list[GuardianModel]:
        stmt = (
            select(GuardianModel)
            .join(GuardianStudentLink, GuardianStudentLink.guardian_id == GuardianModel.id)
            .where(GuardianStudentLink.student_id == student_id)
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def link_to_student(self, guardian_id: UUID, student_id: UUID, relationship: str) -> None:
        link = GuardianStudentLink(guardian_id=guardian_id, student_id=student_id, relationship=relationship)
        self._session.add(link)
        await self._session.flush()

    async def update(self, guardian: GuardianModel) -> GuardianModel:
        await self._session.flush()
        await self._session.refresh(guardian)
        return guardian
