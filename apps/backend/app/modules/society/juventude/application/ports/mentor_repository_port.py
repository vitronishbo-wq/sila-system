from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from apps.backend.app.modules.society.juventude.domain.enums import StatusMentoria
from apps.backend.app.modules.society.juventude.domain.models.mentor import Mentor


class MentorRepositoryPort(ABC):
    @abstractmethod
    async def save(self, mentor: Mentor) -> Mentor:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, mentor_id: UUID) -> Mentor | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_codigo(self, codigo_mentor: str) -> Mentor | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[Mentor]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_status(self, status: StatusMentoria) -> list[Mentor]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, mentor_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def next_codigo(self) -> str:
        raise NotImplementedError
