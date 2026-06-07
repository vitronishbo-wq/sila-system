from abc import ABC, abstractmethod
from uuid import UUID

from apps.backend.app.modules.educacao.infrastructure.models.guardian_model import GuardianModel


class GuardianRepositoryPort(ABC):
    @abstractmethod
    async def create(self, guardian: GuardianModel) -> GuardianModel:
        pass

    @abstractmethod
    async def get_by_id(self, guardian_id: UUID) -> GuardianModel | None:
        pass

    @abstractmethod
    async def find_by_document(self, document_id: str) -> list[GuardianModel]:
        pass

    @abstractmethod
    async def find_by_student(self, student_id: UUID) -> list[GuardianModel]:
        pass

    @abstractmethod
    async def link_to_student(self, guardian_id: UUID, student_id: UUID, relationship: str) -> None:
        pass

    @abstractmethod
    async def update(self, guardian: GuardianModel) -> GuardianModel:
        pass
