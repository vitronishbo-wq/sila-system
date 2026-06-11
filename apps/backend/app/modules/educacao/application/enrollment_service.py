from __future__ import annotations

from datetime import date
from uuid import UUID, uuid4

from apps.backend.app.core.bridges import CitizenRepositoryPort, ServiceRequestLifecycleBridge
from apps.backend.app.modules.educacao.application.ports import (
    EscolaRepositoryPort,
    TurmaRepositoryPort,
    EnrollmentRepositoryPort,
)
from apps.backend.app.modules.educacao.domain.models.enrollment import Enrollment
from apps.backend.app.modules.educacao.exceptions import (
    CitizenNotFoundError,
    EscolaNotFoundError,
    IdadeMinimaNaoAtendidaError,
    InvalidMatriculaStateError,
    MatriculaAlreadyExistsError,
    TurmaNotFoundError,
    TurmaSemVagasError,
)


class EnrollmentService:
    def __init__(
        self,
        enrollment_repo: EnrollmentRepositoryPort,
        turma_repo: TurmaRepositoryPort,
        escola_repo: EscolaRepositoryPort,
        citizen_repo: CitizenRepositoryPort,
        request_service: ServiceRequestLifecycleBridge,
    ):
        self.enrollment_repo = enrollment_repo
        self.turma_repo = turma_repo
        self.escola_repo = escola_repo
        self.citizen_repo = citizen_repo
        self.request_service = request_service

    async def create_enrollment(
        self,
        *,
        student_id: UUID,
        institution_id: UUID,
        academic_year: str,
        grade: str | None = None,
    ) -> Enrollment:
        # Basic validation
        citizen = await self.citizen_repo.get_by_id(student_id)
        if not citizen:
            raise CitizenNotFoundError(f"Cidadão {student_id} não encontrado")

        institution = await self.escola_repo.get_by_id(institution_id)
        if not institution:
            raise EscolaNotFoundError(f"Escola {institution_id} não encontrada")

        # Check for existing enrollment
        exists = await self.enrollment_repo.find_active_by_student_and_year(student_id, academic_year)
        if exists:
            raise MatriculaAlreadyExistsError(
                "Cidadão já possui matrícula ativa/pendente no ano letivo informado"
            )

        # Create new enrollment
        enrollment = Enrollment(
            student_id=student_id,
            institution_id=institution_id,
            academic_year=academic_year,
            grade=grade,
        )

        # Save and return
        return await self.enrollment_repo.save(enrollment)

    async def activate_enrollment(self, enrollment_id: UUID) -> Enrollment:
        enrollment = await self.enrollment_repo.get_by_id(enrollment_id)
        if not enrollment:
            raise InvalidMatriculaStateError("Matrícula não encontrada")
        
        enrollment.activate()

        return await self.enrollment_repo.save(enrollment)

    async def cancel_enrollment(self, enrollment_id: UUID) -> Enrollment:
        enrollment = await self.enrollment_repo.get_by_id(enrollment_id)
        if not enrollment:
            raise InvalidMatriculaStateError("Matrícula não encontrada")
        
        enrollment.cancel()

        return await self.enrollment_repo.save(enrollment)
