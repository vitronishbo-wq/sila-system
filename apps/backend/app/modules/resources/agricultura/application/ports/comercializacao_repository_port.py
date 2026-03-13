from __future__ import annotations
from abc import ABC, abstractmethod
from apps.backend.app.modules.resources.agricultura.domain.models.comercializacao import Comercializacao

class ComercializacaoRepositoryPort(ABC):

    @abstractmethod
    async def save(self, item: Comercializacao) -> Comercializacao:
        pass

    @abstractmethod
    async def get_by_codigo(self, codigo_comercializacao: str) -> Comercializacao | None:
        pass

    @abstractmethod
    async def list(self, *, codigo_safra: str | None=None) -> list[Comercializacao]:
        pass

    @abstractmethod
    async def next_codigo(self) -> str:
        pass