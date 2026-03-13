from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.models.assinante import Assinante

class AssinanteRepositoryPort(ABC):

    @abstractmethod
    async def save(self, assinante: Assinante) -> Assinante:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, assinante_id: UUID) -> Assinante | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_codigo(self, codigo_assinante: str) -> Assinante | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_citizen(self, citizen_id: UUID) -> Assinante | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[Assinante]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_operadora(self, operadora_id: UUID) -> list[Assinante]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_municipio(self, municipio: str) -> list[Assinante]:
        raise NotImplementedError

    @abstractmethod
    async def list_ativos(self) -> list[Assinante]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, assinante_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def next_codigo(self) -> str:
        raise NotImplementedError