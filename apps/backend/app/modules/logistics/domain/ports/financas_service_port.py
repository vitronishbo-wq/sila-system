from __future__ import annotations

from abc import ABC, abstractmethod
from decimal import Decimal
from uuid import UUID


class FinancasServicePort(ABC):
    @abstractmethod
    async def validar_tarifa(self, *, valor: Decimal, tipo: str) -> bool:
        pass

    @abstractmethod
    async def registrar_despesa_manutencao(
        self, *, frota_id: UUID, veiculo_id: UUID, valor: Decimal, descricao: str
    ) -> bool:
        pass

    @abstractmethod
    async def registrar_receita_bilhetagem(
        self, *, evento_id: UUID, valor: Decimal, forma_pagamento: str
    ) -> str:
        pass

    @abstractmethod
    async def reconciliar_lancamento(
        self, *, lancamento_id: str, confirmado: bool, referencia_externa: str | None = None
    ) -> bool:
        pass
