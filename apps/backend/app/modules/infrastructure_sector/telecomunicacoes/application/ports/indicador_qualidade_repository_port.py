from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.enums import (
    StatusIndicadorQualidade,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.models.indicador_qualidade import (
    IndicadorQualidade,
)


class IndicadorQualidadeRepositoryPort(ABC):
    @abstractmethod
    async def save(self, indicador: IndicadorQualidade) -> IndicadorQualidade:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, indicador_id: UUID) -> IndicadorQualidade | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_codigo(self, codigo_indicador: str) -> IndicadorQualidade | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_operadora_periodo(
        self, operadora_id: UUID, referencia_ano: int, referencia_mes: int
    ) -> IndicadorQualidade | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[IndicadorQualidade]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_operadora(self, operadora_id: UUID) -> list[IndicadorQualidade]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_status(self, status: StatusIndicadorQualidade) -> list[IndicadorQualidade]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, indicador_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def next_codigo(self) -> str:
        raise NotImplementedError
