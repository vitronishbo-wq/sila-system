from __future__ import annotations

from uuid import UUID

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.educacao.application.ports import EnrollmentRepositoryPort
from apps.backend.app.modules.educacao.infrastructure.models.enrollment_model import EnrollmentModel


class SQLAlchemyEnrollmentRepository(EnrollmentRepositoryPort):
    """Repositório real para EnrollmentModel com rastreamento histórico e linhagem de transferências."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, enrollment_data: dict) -> dict:
        """Salvar matrícula com validação de UNIQUE constraint (student_id, academic_year)."""
        model = await self.session.get(EnrollmentModel, enrollment_data.get("id"))
        if not model:
            model = EnrollmentModel(id=enrollment_data.get("id"))
            self.session.add(model)

        model.student_id = enrollment_data.get("student_id")
        model.institution_id = enrollment_data.get("institution_id")
        model.academic_year = enrollment_data.get("academic_year")
        model.grade = enrollment_data.get("grade")
        model.status = enrollment_data.get("status", "ACTIVE")
        model.started_at = enrollment_data.get("started_at")
        model.ended_at = enrollment_data.get("ended_at")
        model.transfer_origin_id = enrollment_data.get("transfer_origin_id")
        model.transfer_destination_id = enrollment_data.get("transfer_destination_id")
        model.territory_id = enrollment_data.get("territory_id")
        model.created_by = enrollment_data.get("created_by")
        model.managed_by = enrollment_data.get("managed_by")

        await self.session.flush()
        await self.session.refresh(model)
        return self._to_dict(model)

    async def get_by_id(self, id: UUID) -> dict | None:
        """Obter matrícula por UUID."""
        model = await self.session.get(EnrollmentModel, id)
        return self._to_dict(model) if model else None

    async def get_by_student(self, student_id: UUID) -> list[dict]:
        """Listar todas as matrículas de um estudante (histórico)."""
        stmt = select(EnrollmentModel).where(EnrollmentModel.student_id == student_id)
        models = (await self.session.execute(stmt)).scalars().all()
        return [self._to_dict(m) for m in models]

    async def get_by_institution_year(self, institution_id: UUID, academic_year: str) -> list[dict]:
        """Listar matrículas de uma instituição em um ano letivo."""
        stmt = select(EnrollmentModel).where(
            and_(
                EnrollmentModel.institution_id == institution_id,
                EnrollmentModel.academic_year == academic_year,
            )
        )
        models = (await self.session.execute(stmt)).scalars().all()
        return [self._to_dict(m) for m in models]

    async def get_by_status(self, status: str) -> list[dict]:
        """Listar matrículas por status (ACTIVE, COMPLETED, TRANSFERRED, etc)."""
        stmt = select(EnrollmentModel).where(EnrollmentModel.status == status)
        models = (await self.session.execute(stmt)).scalars().all()
        return [self._to_dict(m) for m in models]

    async def list_student_history(self, student_id: UUID) -> list[dict]:
        """Listar histórico completo de matrículas de um estudante ordenado por data."""
        stmt = (
            select(EnrollmentModel)
            .where(EnrollmentModel.student_id == student_id)
            .order_by(EnrollmentModel.started_at.desc())
        )
        models = (await self.session.execute(stmt)).scalars().all()
        return [self._to_dict(m) for m in models]

    async def exists_active_enrollment(self, student_id: UUID, academic_year: str) -> bool:
        """Verificar se estudante tem matrícula ativa no ano letivo."""
        stmt = select(EnrollmentModel.id).where(
            and_(
                EnrollmentModel.student_id == student_id,
                EnrollmentModel.academic_year == academic_year,
                EnrollmentModel.status.in_(["ACTIVE", "PENDING"]),
            )
        )
        return (await self.session.execute(stmt)).first() is not None

    async def get_by_transfer_origin(self, transfer_id: UUID) -> dict | None:
        """Obter matrícula originária de uma transferência."""
        stmt = select(EnrollmentModel).where(EnrollmentModel.transfer_origin_id == transfer_id)
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_dict(model) if model else None

    async def update_status(self, id: UUID, status: str) -> dict | None:
        """Atualizar status de uma matrícula."""
        model = await self.session.get(EnrollmentModel, id)
        if not model:
            return None

        model.status = status
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_dict(model)

    def _to_dict(self, model: EnrollmentModel | None) -> dict | None:
        """Converter modelo SQLAlchemy para dict."""
        if not model:
            return None
        return {
            "id": model.id,
            "student_id": model.student_id,
            "institution_id": model.institution_id,
            "academic_year": model.academic_year,
            "grade": model.grade,
            "status": model.status,
            "started_at": model.started_at,
            "ended_at": model.ended_at,
            "transfer_origin_id": model.transfer_origin_id,
            "transfer_destination_id": model.transfer_destination_id,
            "territory_id": model.territory_id,
            "created_by": model.created_by,
            "managed_by": model.managed_by,
            "created_at": model.created_at,
            "updated_at": model.updated_at,
        }
