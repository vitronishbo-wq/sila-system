from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from apps.backend.app.modules.educacao.domain.wizard_session import WizardSession


class WizardSessionRepositoryPort(ABC):
    @abstractmethod
    async def save(self, session: WizardSession) -> WizardSession:
        ...

    @abstractmethod
    async def get_by_id(self, session_id: UUID) -> WizardSession | None:
        ...

    @abstractmethod
    async def get_active_by_citizen(
        self, citizen_id: UUID
    ) -> list[WizardSession]:
        ...

    @abstractmethod
    async def expire_stale(self) -> int:
        ...
