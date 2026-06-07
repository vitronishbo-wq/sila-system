from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from apps.backend.app.modules.public_security.domain.enums import StatusAgente, TipoAgente
from apps.backend.app.modules.public_security.domain.models.policial import Policial


class PolicialRepositoryPort(ABC):
    @abstractmethod
    async def save(self, policial: Policial) -> Policial:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, policial_id: UUID) -> Policial | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_matricula(self, matricula: str) -> Policial | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_cpf(self, cpf: str) -> Policial | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[Policial]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_unidade(self, unidade_id: UUID) -> list[Policial]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_tipo(self, tipo: TipoAgente) -> list[Policial]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_status(self, status: StatusAgente) -> list[Policial]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, policial_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def next_matricula(self, unidade_id: UUID) -> str:
        raise NotImplementedError
