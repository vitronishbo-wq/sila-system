from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from apps.backend.app.modules.society.desporto.domain.enums import StatusTransferencia
from apps.backend.app.modules.society.desporto.domain.models.transferencia import Transferencia


class TransferenciaRepositoryPort(ABC):
    @abstractmethod
    async def save(self, transferencia: Transferencia) -> Transferencia:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, transferencia_id: UUID) -> Transferencia | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_codigo(self, codigo_transferencia: str) -> Transferencia | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[Transferencia]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_atleta(self, atleta_id: UUID) -> list[Transferencia]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_status(self, status: StatusTransferencia) -> list[Transferencia]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, transferencia_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def next_codigo(self) -> str:
        raise NotImplementedError
