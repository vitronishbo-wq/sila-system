from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from apps.backend.app.modules.society.juventude.domain.enums import StatusAcompanhamento
from apps.backend.app.modules.society.juventude.domain.models.saude_juvenil import SaudeJuvenil

class SaudeJuvenilRepositoryPort(ABC):

    @abstractmethod
    async def save(self, registo: SaudeJuvenil) -> SaudeJuvenil:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, registo_id: UUID) -> SaudeJuvenil | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_codigo(self, codigo_registo: str) -> SaudeJuvenil | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[SaudeJuvenil]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_jovem(self, jovem_id: UUID) -> list[SaudeJuvenil]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_status(self, status: StatusAcompanhamento) -> list[SaudeJuvenil]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, registo_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def next_codigo(self) -> str:
        raise NotImplementedError