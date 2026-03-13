from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from apps.backend.app.modules.infrastructure_sector.meteorologia.domain.enums import StationStatus
from apps.backend.app.modules.infrastructure_sector.meteorologia.domain.models import EstacaoMeteorologica

class EstacaoRepositoryPort(ABC):

    @abstractmethod
    async def save(self, estacao: EstacaoMeteorologica) -> EstacaoMeteorologica:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, estacao_id: UUID) -> EstacaoMeteorologica | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_codigo(self, codigo: str) -> EstacaoMeteorologica | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self, limit: int=100, offset: int=0) -> list[EstacaoMeteorologica]:
        raise NotImplementedError

    @abstractmethod
    async def list_active(self, provincia: str | None=None) -> list[EstacaoMeteorologica]:
        raise NotImplementedError

    @abstractmethod
    async def list_filtered(self, *, provincia: str | None=None, status: StationStatus | None=None, limit: int=100, offset: int=0) -> list[EstacaoMeteorologica]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, estacao_id: UUID) -> bool:
        raise NotImplementedError