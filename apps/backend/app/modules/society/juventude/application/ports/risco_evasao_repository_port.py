from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from apps.backend.app.modules.society.juventude.domain.enums import RiscoSocial
from apps.backend.app.modules.society.juventude.domain.models.risco_evasao import RiscoEvasao


class RiscoEvasaoRepositoryPort(ABC):
    @abstractmethod
    async def save(self, risco: RiscoEvasao) -> RiscoEvasao:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, risco_id: UUID) -> RiscoEvasao | None:
        raise NotImplementedError

    @abstractmethod
    async def get_ativo_by_jovem(self, jovem_id: UUID) -> RiscoEvasao | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[RiscoEvasao]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_nivel(self, nivel: RiscoSocial) -> list[RiscoEvasao]:
        raise NotImplementedError

    @abstractmethod
    async def next_codigo(self) -> str:
        raise NotImplementedError
