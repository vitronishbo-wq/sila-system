from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from app.modules.infrastructure_sector.telecomunicacoes.domain.enums import StatusOutorga
from app.modules.infrastructure_sector.telecomunicacoes.domain.models.outorga_espectro import OutorgaEspectro

class OutorgaEspectroRepositoryPort(ABC):

    @abstractmethod
    async def save(self, outorga: OutorgaEspectro) -> OutorgaEspectro:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, outorga_id: UUID) -> OutorgaEspectro | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_numero(self, numero_outorga: str) -> OutorgaEspectro | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[OutorgaEspectro]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_operadora(self, operadora_id: UUID) -> list[OutorgaEspectro]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_status(self, status: StatusOutorga) -> list[OutorgaEspectro]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, outorga_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def next_numero(self) -> str:
        raise NotImplementedError