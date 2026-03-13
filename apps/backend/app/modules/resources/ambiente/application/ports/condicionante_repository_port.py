from __future__ import annotations
from abc import ABC, abstractmethod
from apps.backend.app.modules.resources.ambiente.domain.enums import StatusCondicionante
from apps.backend.app.modules.resources.ambiente.domain.models.condicionante import Condicionante

class CondicionanteRepositoryPort(ABC):

    @abstractmethod
    async def save(self, item: Condicionante) -> Condicionante:
        pass

    @abstractmethod
    async def get_by_codigo(self, codigo_condicionante: str) -> Condicionante | None:
        pass

    @abstractmethod
    async def list(self, *, numero_licenca: str | None=None, status: StatusCondicionante | None=None) -> list[Condicionante]:
        pass

    @abstractmethod
    async def next_codigo(self) -> str:
        pass