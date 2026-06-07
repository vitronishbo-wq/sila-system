from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from apps.backend.app.modules.logistics.domain.ports.financas_service_port import (
    FinancasServicePort,
)


class FinancasServiceAdapter(FinancasServicePort):
    async def validar_tarifa(self, *, valor: Decimal, tipo: str) -> bool:
        return valor > Decimal("0") and bool(tipo.strip())

    async def registrar_despesa_manutencao(
        self, *, frota_id: UUID, veiculo_id: UUID, valor: Decimal, descricao: str
    ) -> bool:
        _ = (frota_id, veiculo_id, descricao)
        return valor > Decimal("0")

    async def registrar_receita_bilhetagem(
        self, *, evento_id: UUID, valor: Decimal, forma_pagamento: str
    ) -> str:
        if valor <= Decimal("0"):
            raise ValueError("Valor de bilhetagem deve ser maior que zero")
        if not forma_pagamento.strip():
            raise ValueError("Forma de pagamento obrigatoria para receita de bilhetagem")
        return f"REC-TRN-{str(evento_id)[:8].upper()}"

    async def reconciliar_lancamento(
        self, *, lancamento_id: str, confirmado: bool, referencia_externa: str | None = None
    ) -> bool:
        _ = (confirmado, referencia_externa)
        return bool(lancamento_id.strip())
