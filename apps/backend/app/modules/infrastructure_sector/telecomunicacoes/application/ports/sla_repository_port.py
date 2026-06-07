from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.enums import (
    StatusSLA,
    TipoServico,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.models.sla import SLA


class SLARepositoryPort(ABC):
    @abstractmethod
    async def save(self, sla: SLA) -> SLA:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, sla_id: UUID) -> SLA | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_codigo(self, codigo_sla: str) -> SLA | None:
        raise NotImplementedError

    @abstractmethod
    async def find_ativo_por_operadora_servico(
        self, operadora_id: UUID, servico: TipoServico
    ) -> SLA | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[SLA]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_operadora(self, operadora_id: UUID) -> list[SLA]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_status(self, status: StatusSLA) -> list[SLA]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, sla_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def next_codigo(self) -> str:
        raise NotImplementedError
