from __future__ import annotations

from abc import ABC, abstractmethod

from apps.backend.app.modules.resources.agricultura.domain.enums import StatusCredito
from apps.backend.app.modules.resources.agricultura.domain.models.credito_rural import CreditoRural


class CreditoRepositoryPort(ABC):
    @abstractmethod
    async def save(self, item: CreditoRural) -> CreditoRural:
        pass

    @abstractmethod
    async def get_by_codigo(self, codigo_credito: str) -> CreditoRural | None:
        pass

    @abstractmethod
    async def list(
        self, *, codigo_produtor: str | None = None, status: StatusCredito | None = None
    ) -> list[CreditoRural]:
        pass

    @abstractmethod
    async def next_codigo(self) -> str:
        pass
