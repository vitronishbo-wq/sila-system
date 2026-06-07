from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date
from uuid import UUID

from apps.backend.app.modules.resources.pescas.industrial.domain.enums import StatusLoteProducao
from apps.backend.app.modules.resources.pescas.industrial.domain.models.lote_producao import (
    LoteProducao,
)


class LoteProducaoRepositoryPort(ABC):
    @abstractmethod
    async def save(self, lote: LoteProducao) -> LoteProducao:
        pass

    @abstractmethod
    async def get_by_id(self, lote_id: UUID) -> LoteProducao | None:
        pass

    @abstractmethod
    async def get_by_codigo(self, codigo_lote: str) -> LoteProducao | None:
        pass

    @abstractmethod
    async def list_all(self) -> list[LoteProducao]:
        pass

    @abstractmethod
    async def list_by_unidade(self, unidade_processamento_id: UUID) -> list[LoteProducao]:
        pass

    @abstractmethod
    async def list_by_produto(self, produto_processado_id: UUID) -> list[LoteProducao]:
        pass

    @abstractmethod
    async def list_by_status(self, status: StatusLoteProducao) -> list[LoteProducao]:
        pass

    @abstractmethod
    async def list_by_periodo(self, data_inicio: date, data_fim: date) -> list[LoteProducao]:
        pass

    @abstractmethod
    async def delete(self, lote_id: UUID) -> bool:
        pass

    @abstractmethod
    async def next_codigo(self) -> str:
        pass
