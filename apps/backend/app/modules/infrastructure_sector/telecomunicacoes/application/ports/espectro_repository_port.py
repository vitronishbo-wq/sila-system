from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.enums import StatusEspectro, TipoEspectro
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.models.espectro import Espectro

class EspectroRepositoryPort(ABC):

    @abstractmethod
    async def save(self, espectro: Espectro) -> Espectro:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, espectro_id: UUID) -> Espectro | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_codigo(self, codigo_espectro: str) -> Espectro | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[Espectro]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_tipo(self, tipo: TipoEspectro) -> list[Espectro]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_municipio(self, municipio: str) -> list[Espectro]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_status(self, status: StatusEspectro) -> list[Espectro]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, espectro_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def next_codigo(self) -> str:
        raise NotImplementedError