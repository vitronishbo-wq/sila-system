from __future__ import annotations

from abc import ABC, abstractmethod

from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.domain.models.georreferenciamento import (
    Georreferenciamento,
)


class GeorreferenciamentoRepositoryPort(ABC):
    @abstractmethod
    async def save(self, item: Georreferenciamento) -> Georreferenciamento:
        pass

    @abstractmethod
    async def get_by_codigo(self, codigo_geo: str) -> Georreferenciamento | None:
        pass

    @abstractmethod
    async def list(
        self,
        *,
        imovel_inscricao: str | None = None,
        validado: bool | None = None,
        ativo: bool | None = None,
    ) -> list[Georreferenciamento]:
        pass

    @abstractmethod
    async def next_codigo(self) -> str:
        pass
