from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from uuid import UUID

from apps.backend.app.modules.economy.trade.external.domain.enums import StatusHabilitacao
from apps.backend.app.modules.economy.trade.external.domain.models.operador_logistico_base import (
    OperadorLogisticoBase,
)

TOperadorLogistico = TypeVar("TOperadorLogistico", bound=OperadorLogisticoBase)


class OperadorLogisticoRepositoryPort(ABC, Generic[TOperadorLogistico]):
    @abstractmethod
    async def save(self, operador: TOperadorLogistico) -> TOperadorLogistico:
        pass

    @abstractmethod
    async def get_by_id(self, id: UUID) -> TOperadorLogistico | None:
        pass

    @abstractmethod
    async def get_by_cnpj_cpf(self, cnpj_cpf: str) -> TOperadorLogistico | None:
        pass

    @abstractmethod
    async def list(
        self, *, status: StatusHabilitacao | None = None, municipio: str | None = None
    ) -> list[TOperadorLogistico]:
        pass
