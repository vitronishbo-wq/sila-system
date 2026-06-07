from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.models.infraestrutura_telco import (
    InfraestruturaTelco,
)


class InfraestruturaRepositoryPort(ABC):
    @abstractmethod
    async def save(self, infraestrutura: InfraestruturaTelco) -> InfraestruturaTelco:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, infraestrutura_id: UUID) -> InfraestruturaTelco | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_codigo(self, codigo_infra: str) -> InfraestruturaTelco | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[InfraestruturaTelco]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_operadora(self, operadora_id: UUID) -> list[InfraestruturaTelco]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_municipio(self, municipio: str) -> list[InfraestruturaTelco]:
        raise NotImplementedError

    @abstractmethod
    async def list_ativas(self) -> list[InfraestruturaTelco]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, infraestrutura_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def next_codigo(self) -> str:
        raise NotImplementedError
