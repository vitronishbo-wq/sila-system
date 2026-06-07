from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from apps.backend.app.modules.civil_protection.domain.enums import StatusAgenteProtecao
from apps.backend.app.modules.civil_protection.domain.models.bombeiro import Bombeiro


class BombeiroRepositoryPort(ABC):
    @abstractmethod
    async def save(self, bombeiro: Bombeiro) -> Bombeiro:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, bombeiro_id: UUID) -> Bombeiro | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_matricula(self, matricula: str) -> Bombeiro | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_cpf(self, cpf: str) -> Bombeiro | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[Bombeiro]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_corporacao(self, corporacao_id: UUID) -> list[Bombeiro]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_status(self, status: StatusAgenteProtecao) -> list[Bombeiro]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, bombeiro_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def next_matricula(self, corporacao_id: UUID) -> str:
        raise NotImplementedError
