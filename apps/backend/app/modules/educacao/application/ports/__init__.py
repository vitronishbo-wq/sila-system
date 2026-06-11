from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID

from apps.backend.app.modules.educacao.domain.models.enrollment import Enrollment


class EnrollmentRepositoryPort(ABC):

    @abstractmethod
    async def save(self, enrollment: Enrollment) -> Enrollment:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Enrollment | None:
        raise NotImplementedError

    @abstractmethod
    async def find_active_by_student_and_year(self, student_id: UUID, academic_year: str) -> Enrollment | None:
        raise NotImplementedError
