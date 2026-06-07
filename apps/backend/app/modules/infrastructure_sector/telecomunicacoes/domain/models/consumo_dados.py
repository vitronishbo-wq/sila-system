from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4


@dataclass
class ConsumoDados:
    id: UUID
    assinante_id: UUID
    referencia: str
    dados_up_gb: Decimal
    dados_down_gb: Decimal
    tecnologia: str
    periodo_inicio: datetime | None
    periodo_fim: datetime | None
    created_at: datetime

    @classmethod
    def registrar(
        cls,
        *,
        assinante_id: UUID,
        referencia: str,
        dados_up_gb: Decimal,
        dados_down_gb: Decimal,
        tecnologia: str,
        periodo_inicio: datetime | None,
        periodo_fim: datetime | None,
    ) -> ConsumoDados:
        if dados_up_gb < Decimal("0") or dados_down_gb < Decimal("0"):
            raise ValueError("Consumo nao pode ser negativo")
        if not referencia.strip():
            raise ValueError("Referencia obrigatoria")
        if not tecnologia.strip():
            raise ValueError("Tecnologia obrigatoria")
        return cls(
            id=uuid4(),
            assinante_id=assinante_id,
            referencia=referencia.strip(),
            dados_up_gb=dados_up_gb.quantize(Decimal("0.01")),
            dados_down_gb=dados_down_gb.quantize(Decimal("0.01")),
            tecnologia=tecnologia.strip().upper(),
            periodo_inicio=periodo_inicio,
            periodo_fim=periodo_fim,
            created_at=datetime.utcnow(),
        )

    @property
    def total_gb(self) -> Decimal:
        return (self.dados_up_gb + self.dados_down_gb).quantize(Decimal("0.01"))
