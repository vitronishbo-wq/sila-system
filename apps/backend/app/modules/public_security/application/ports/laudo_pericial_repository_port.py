from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from apps.backend.app.modules.public_security.domain.enums import StatusLaudo, TipoLaudo
from apps.backend.app.modules.public_security.domain.models.laudo_pericial import LaudoPericial


class LaudoPericialRepositoryPort(ABC):
    @abstractmethod
    async def save(self, laudo: LaudoPericial) -> LaudoPericial:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, laudo_id: UUID) -> LaudoPericial | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_numero(self, numero_laudo: str) -> LaudoPericial | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[LaudoPericial]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_prova(self, prova_id: UUID) -> list[LaudoPericial]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_tipo(self, tipo: TipoLaudo) -> list[LaudoPericial]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_status(self, status: StatusLaudo) -> list[LaudoPericial]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, laudo_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def next_numero(self) -> str:
        raise NotImplementedError
