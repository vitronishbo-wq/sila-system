from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from apps.backend.app.modules.society.assistencia_social.domain.models import SituacaoRua


class SituacaoRuaRepositoryPort(ABC):
    @abstractmethod
    async def save(self, entity: SituacaoRua) -> SituacaoRua:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, entity_id: UUID) -> SituacaoRua | None:
        raise NotImplementedError

    @abstractmethod
    async def list_by_beneficiario(self, beneficiario_id: UUID) -> list[SituacaoRua]:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[SituacaoRua]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, entity_id: UUID) -> bool:
        raise NotImplementedError
