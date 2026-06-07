from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date
from decimal import Decimal
from uuid import UUID


class FinancasGatewayPort(ABC):
    @abstractmethod
    async def registrar_fatura_agua(
        self,
        *,
        fatura_id: UUID,
        numero_fatura: str,
        titular_id: UUID,
        referencia: str,
        valor_total: Decimal,
        data_emissao: date,
        data_vencimento: date,
    ) -> str:
        pass

    @abstractmethod
    async def registrar_pagamento_fatura_agua(
        self,
        *,
        fatura_id: UUID,
        numero_fatura: str,
        titular_id: UUID,
        valor_pago: Decimal,
        data_pagamento: date,
        metodo_pagamento: str,
    ) -> str:
        pass
