from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID


class EnrollmentRepositoryPort(ABC):
    """Porta para persistencia de matriculações com rastreamento histórico e linhagem de transferências."""

    @abstractmethod
    async def save(self, enrollment_data: dict) -> dict:
        """Salvar matrícula com validação de UNIQUE constraint (student_id, academic_year)."""
        pass

    @abstractmethod
    async def get_by_id(self, id: UUID) -> dict | None:
        """Obter matrícula por UUID."""
        pass

    @abstractmethod
    async def get_by_student(self, student_id: UUID) -> list[dict]:
        """Listar todas as matrículas de um estudante (histórico)."""
        pass

    @abstractmethod
    async def get_by_institution_year(self, institution_id: UUID, academic_year: str) -> list[dict]:
        """Listar matrículas de uma instituição em um ano letivo."""
        pass

    @abstractmethod
    async def get_by_status(self, status: str) -> list[dict]:
        """Listar matrículas por status (ACTIVE, COMPLETED, TRANSFERRED, etc)."""
        pass

    @abstractmethod
    async def list_student_history(self, student_id: UUID) -> list[dict]:
        """Listar histórico completo de matrículas de um estudante ordenado por data."""
        pass

    @abstractmethod
    async def exists_active_enrollment(self, student_id: UUID, academic_year: str) -> bool:
        """Verificar se estudante tem matrícula ativa no ano letivo."""
        pass

    @abstractmethod
    async def get_by_transfer_origin(self, transfer_id: UUID) -> dict | None:
        """Obter matrícula originária de uma transferência."""
        pass

    @abstractmethod
    async def update_status(self, id: UUID, status: str) -> dict | None:
        """Atualizar status de uma matrícula."""
        pass
