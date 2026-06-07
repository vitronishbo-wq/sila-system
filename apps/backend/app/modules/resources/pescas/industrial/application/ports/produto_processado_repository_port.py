from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from apps.backend.app.modules.resources.pescas.industrial.domain.enums import (
    MercadoDestino,
    TipoProdutoProcessado,
)
from apps.backend.app.modules.resources.pescas.industrial.domain.models.produto_processado import (
    ProdutoProcessado,
)


class ProdutoProcessadoRepositoryPort(ABC):
    @abstractmethod
    async def save(self, produto: ProdutoProcessado) -> ProdutoProcessado:
        pass

    @abstractmethod
    async def get_by_id(self, produto_id: UUID) -> ProdutoProcessado | None:
        pass

    @abstractmethod
    async def get_by_codigo(self, codigo_produto: str) -> ProdutoProcessado | None:
        pass

    @abstractmethod
    async def list_all(self) -> list[ProdutoProcessado]:
        pass

    @abstractmethod
    async def list_by_unidade(self, unidade_processamento_id: UUID) -> list[ProdutoProcessado]:
        pass

    @abstractmethod
    async def list_by_tipo(self, tipo_produto: TipoProdutoProcessado) -> list[ProdutoProcessado]:
        pass

    @abstractmethod
    async def list_by_destino(self, mercado_destino: MercadoDestino) -> list[ProdutoProcessado]:
        pass

    @abstractmethod
    async def delete(self, produto_id: UUID) -> bool:
        pass

    @abstractmethod
    async def next_codigo(self) -> str:
        pass
