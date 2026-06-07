from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from apps.backend.app.modules.society.desporto.domain.enums import StatusContrato, TipoContrato
from apps.backend.app.modules.society.desporto.domain.models.contrato import Contrato


class ContratoRepositoryPort(ABC):
    @abstractmethod
    async def save(self, contrato: Contrato) -> Contrato:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, contrato_id: UUID) -> Contrato | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_codigo(self, codigo_contrato: str) -> Contrato | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[Contrato]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_atleta(self, atleta_id: UUID) -> list[Contrato]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_clube(self, clube_id: UUID) -> list[Contrato]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_tipo(self, tipo: TipoContrato) -> list[Contrato]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_status(self, status: StatusContrato) -> list[Contrato]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, contrato_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def next_codigo(self) -> str:
        raise NotImplementedError
