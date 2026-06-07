from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from apps.backend.app.modules.public_security.domain.enums import StatusVestigio
from apps.backend.app.modules.public_security.domain.models.vestigio import Vestigio


class VestigioRepositoryPort(ABC):
    @abstractmethod
    async def save(self, vestigio: Vestigio) -> Vestigio:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, vestigio_id: UUID) -> Vestigio | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_codigo(self, codigo_vestigio: str) -> Vestigio | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[Vestigio]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_cadeia(self, cadeia_custodia_id: UUID) -> list[Vestigio]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_status(self, status: StatusVestigio) -> list[Vestigio]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, vestigio_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def next_codigo(self) -> str:
        raise NotImplementedError
