from __future__ import annotations

from abc import ABC, abstractmethod

from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.domain.models.proprietario import (
    Proprietario,
)


class ProprietarioRepositoryPort(ABC):
    @abstractmethod
    async def save(self, item: Proprietario) -> Proprietario:
        pass

    @abstractmethod
    async def get_by_numero_cadastro(self, numero_cadastro: str) -> Proprietario | None:
        pass

    @abstractmethod
    async def get_by_documento(self, documento: str) -> Proprietario | None:
        pass

    @abstractmethod
    async def list(
        self, *, tipo_pessoa: str | None = None, ativo: bool | None = None
    ) -> list[Proprietario]:
        pass

    @abstractmethod
    async def next_numero_cadastro(self) -> str:
        pass
