from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from apps.backend.app.modules.society.assistencia_social.domain.models import IdosoVulneravel


class IdosoVulneravelRepositoryPort(ABC):
    @abstractmethod
    async def save(self, entity: IdosoVulneravel) -> IdosoVulneravel:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, entity_id: UUID) -> IdosoVulneravel | None:
        raise NotImplementedError

    @abstractmethod
    async def list_by_beneficiario(self, beneficiario_id: UUID) -> list[IdosoVulneravel]:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[IdosoVulneravel]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, entity_id: UUID) -> bool:
        raise NotImplementedError
