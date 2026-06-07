from __future__ import annotations

from abc import ABC, abstractmethod

from apps.backend.app.modules.resources.ambiente.domain.enums import StatusMulta
from apps.backend.app.modules.resources.ambiente.domain.models.multa import Multa


class MultaRepositoryPort(ABC):
    @abstractmethod
    async def save(self, item: Multa) -> Multa:
        pass

    @abstractmethod
    async def get_by_numero(self, numero_multa: str) -> Multa | None:
        pass

    @abstractmethod
    async def list(
        self, *, numero_auto_infracao: str | None = None, status: StatusMulta | None = None
    ) -> list[Multa]:
        pass

    @abstractmethod
    async def next_numero(self) -> str:
        pass
