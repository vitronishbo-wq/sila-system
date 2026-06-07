from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.educacao.application.ports import AcademicIdentityRepositoryPort
from apps.backend.app.modules.educacao.infrastructure.models.academic_identity_model import (
    AcademicIdentityModel,
)


class SQLAlchemyAcademicIdentityRepository(AcademicIdentityRepositoryPort):
    """Repositório real para AcademicIdentityModel com persistência transacional."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, identity_data: dict) -> dict:
        """Salvar identidade acadêmica com validação de UNIQUE constraint em national_student_number."""
        model = await self.session.get(AcademicIdentityModel, identity_data.get("id"))
        if not model:
            model = AcademicIdentityModel(id=identity_data.get("id"))
            self.session.add(model)

        model.national_student_number = identity_data.get("national_student_number")
        model.full_name = identity_data.get("full_name")
        model.birth_date = identity_data.get("birth_date")
        model.gender = identity_data.get("gender")
        model.current_institution_id = identity_data.get("current_institution_id")
        model.current_grade = identity_data.get("current_grade")
        model.academic_status = identity_data.get("academic_status", "ACTIVE")
        model.identity_status = identity_data.get("identity_status", "VALID")

        await self.session.flush()
        await self.session.refresh(model)
        return self._to_dict(model)

    async def get_by_id(self, id: UUID) -> dict | None:
        """Obter identidade por UUID."""
        model = await self.session.get(AcademicIdentityModel, id)
        return self._to_dict(model) if model else None

    async def get_by_national_student_number(self, national_student_number: str) -> dict | None:
        """Obter identidade por número de estudante único (UNIQUE constraint)."""
        stmt = select(AcademicIdentityModel).where(
            AcademicIdentityModel.national_student_number == national_student_number
        )
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_dict(model) if model else None

    async def get_by_institution(self, institution_id: UUID) -> list[dict]:
        """Listar estudantes de uma instituição."""
        stmt = select(AcademicIdentityModel).where(
            AcademicIdentityModel.current_institution_id == institution_id
        )
        models = (await self.session.execute(stmt)).scalars().all()
        return [self._to_dict(m) for m in models]

    async def list_by_status(self, status: str) -> list[dict]:
        """Listar identidades por status acadêmico."""
        stmt = select(AcademicIdentityModel).where(AcademicIdentityModel.academic_status == status)
        models = (await self.session.execute(stmt)).scalars().all()
        return [self._to_dict(m) for m in models]

    async def exists_by_national_student_number(self, national_student_number: str) -> bool:
        """Verificar existência de estudante por número único."""
        stmt = select(AcademicIdentityModel.id).where(
            AcademicIdentityModel.national_student_number == national_student_number
        )
        return (await self.session.execute(stmt)).first() is not None

    async def update_status(self, id: UUID, status: str) -> dict | None:
        """Atualizar status acadêmico de uma identidade."""
        model = await self.session.get(AcademicIdentityModel, id)
        if not model:
            return None

        model.academic_status = status
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_dict(model)

    def _to_dict(self, model: AcademicIdentityModel | None) -> dict | None:
        """Converter modelo SQLAlchemy para dict."""
        if not model:
            return None
        return {
            "id": model.id,
            "national_student_number": model.national_student_number,
            "full_name": model.full_name,
            "birth_date": model.birth_date,
            "gender": model.gender,
            "current_institution_id": model.current_institution_id,
            "current_grade": model.current_grade,
            "academic_status": model.academic_status,
            "identity_status": model.identity_status,
            "created_at": model.created_at,
            "updated_at": model.updated_at,
        }
