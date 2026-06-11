from __future__ import annotations

from uuid import UUID
from sqlalchemy.orm import Session

from apps.backend.app.modules.educacao.application.ports import (
    EnrollmentRepositoryPort,
    CapacityRepositoryPort,
)
from apps.backend.app.modules.educacao.domain.models.enrollment import Enrollment
from apps.backend.app.modules.educacao.exceptions import (
    InstitutionCapacityExceededError,
    CapacityUndefinedError,
    MatriculaAlreadyExistsError,
)

class TransactionalEnrollmentService:
    """
    Serviço transacional para orquestrar a criação de matrículas com
    travamento atómico para garantir a integridade da capacidade institucional.
    """
    def __init__(
        self,
        enrollment_repo: EnrollmentRepositoryPort,
        capacity_repo: CapacityRepositoryPort,
    ):
        self.enrollment_repo = enrollment_repo
        self.capacity_repo = capacity_repo

    def enroll_student(
        self,
        session: Session, # A sessão de BD é passada como argumento para garantir a transação única
        *,
        student_id: UUID,
        institution_id: UUID,
        academic_year: str,
        grade: str,
        shift: str,
    ) -> Enrollment:
        """
        Executa o processo de matrícula de ponta a ponta dentro de uma única transação.

        1. Trava a linha de capacidade da instituição/turma.
        2. Valida se ainda existem vagas.
        3. Incrementa o contador de vagas utilizadas.
        4. Cria o registo da matrícula.
        
        Levanta exceções específicas em caso de falha.
        """
        
        # O chamador deste serviço é responsável por gerir o bloco try/except
        # e o commit/rollback da sessão.

        # Passo 1 & 2: Adquirir Lock Pessimista e obter a linha de capacidade
        capacity = self.capacity_repo.get_for_update(
            session=session,
            institution_id=institution_id,
            grade=grade,
            shift=shift,
        )

        # Passo 3: Validar a capacidade
        if not capacity:
            raise CapacityUndefinedError(
                f"Capacidade não definida para a instituição {institution_id} na série {grade} / turno {shift}"
            )

        if capacity.capacity_used >= capacity.capacity_total:
            raise InstitutionCapacityExceededError(
                f"Capacidade máxima atingida para a instituição {institution_id} na série {grade} / turno {shift}"
            )

        # Validar se o estudante já tem uma matrícula (lógica do EnrollmentService original)
        exists = self.enrollment_repo.find_active_by_student_and_year(
            session=session, # A consulta deve usar a mesma sessão transacional
            student_id=student_id,
            academic_year=academic_year
        )
        if exists:
            raise MatriculaAlreadyExistsError(
                "Cidadão já possui matrícula ativa/pendente no ano letivo informado"
            )

        # Passo 4: Incrementar a capacidade utilizada
        capacity.capacity_used += 1

        # Passo 5: Criar e persistir a matrícula
        new_enrollment = Enrollment(
            student_id=student_id,
            institution_id=institution_id,
            academic_year=academic_year,
            grade=grade,
            # O status PENDING é o default do modelo de domínio
        )

        # A persistência ocorre quando a sessão é "commitada" pelo chamador
        session.add(capacity)
        session.add(self.enrollment_repo.to_model(new_enrollment)) # Supondo um método de conversão

        return new_enrollment

