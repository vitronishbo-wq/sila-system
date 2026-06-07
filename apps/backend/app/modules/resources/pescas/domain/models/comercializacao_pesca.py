from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4


@dataclass
class ComercializacaoPesca:
    id: UUID
    produto: str
    quantidade_kg: Decimal
    preco_unitario: Decimal
    data_operacao: date
    comprador: str
    observacoes: str | None = None

    @classmethod
    def registrar(
        cls,
        *,
        produto: str,
        quantidade_kg: Decimal,
        preco_unitario: Decimal,
        data_operacao: date,
        comprador: str,
    ) -> ComercializacaoPesca:
        return cls(
            id=uuid4(),
            produto=produto,
            quantidade_kg=quantidade_kg,
            preco_unitario=preco_unitario,
            data_operacao=data_operacao,
            comprador=comprador,
        )
