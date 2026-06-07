from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from apps.backend.app.modules.tourism.domain.models.agencia_viagens import AgenciaViagens


class AgenciaViagensRepositoryPort(ABC):
    @abstractmethod
    async def save(self, agencia: AgenciaViagens) -> AgenciaViagens:
        pass

    @abstractmethod
    async def get_by_id(self, agencia_id: UUID) -> AgenciaViagens | None:
        pass

    @abstractmethod
    async def get_by_cnpj(self, cnpj: str) -> AgenciaViagens | None:
        pass

    @abstractmethod
    async def get_by_registro(self, registro: str) -> AgenciaViagens | None:
        pass

    @abstractmethod
    async def list(
        self, *, municipio: str | None = None, ativa: bool | None = None
    ) -> list[AgenciaViagens]:
        pass

    @abstractmethod
    async def delete(self, agencia_id: UUID) -> bool:
        pass

    @abstractmethod
    async def next_registro(self, provincia: str) -> str:
        pass
