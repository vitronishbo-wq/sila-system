from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID


class AcademicIdentityRepositoryPort(ABC):
    """Porta para persistencia de identidades acadêmicas (núcleo do sistema inteiro)."""

    @abstractmethod
    async def save(self, identity_data: dict) -> dict:
        """Salvar identidade acadêmica com validação de UNIQUE constraint."""
        pass

    @abstractmethod
    async def get_by_id(self, id: UUID) -> dict | None:
        """Obter identidade por UUID."""
        pass

    @abstractmethod
    async def get_by_national_student_number(self, national_student_number: str) -> dict | None:
        """Obter identidade por número de estudante único."""
        pass

    @abstractmethod
    async def get_by_institution(self, institution_id: UUID) -> list[dict]:
        """Listar estudantes de uma instituição."""
        pass

    @abstractmethod
    async def list_by_status(self, status: str) -> list[dict]:
        """Listar identidades por status acadêmico."""
        pass

    @abstractmethod
    async def exists_by_national_student_number(self, national_student_number: str) -> bool:
        """Verificar existência de estudante por número único."""
        pass

    @abstractmethod
    async def update_status(self, id: UUID, status: str) -> dict | None:
        """Atualizar status acadêmico de uma identidade."""
        pass
