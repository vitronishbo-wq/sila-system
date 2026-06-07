from __future__ import annotations

from abc import ABC, abstractmethod
from decimal import Decimal
from uuid import UUID

from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import (
    TipoAlvara,
)


class FinancasServicePort(ABC):
    @abstractmethod
    async def calcular_taxa_loteamento(
        self, *, area_total: Decimal, quantidade_lotes: int
    ) -> Decimal:
        pass

    @abstractmethod
    async def calcular_taxa_licenciamento(
        self, *, tipo_alvara: TipoAlvara, area_construida_prevista: Decimal | None
    ) -> Decimal:
        pass

    @abstractmethod
    async def registrar_cobranca(
        self, *, referencia_id: UUID, descricao: str, valor: Decimal
    ) -> str:
        pass
