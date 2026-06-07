from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4


@dataclass
class ProducaoPesca:
    id: UUID
    data_producao: date
    quantidade_kg: Decimal
    unidade_processamento: str
    destino: str
    observacoes: str | None = None

    @classmethod
    def registrar(
        cls,
        *,
        data_producao: date,
        quantidade_kg: Decimal,
        unidade_processamento: str,
        destino: str,
    ) -> ProducaoPesca:
        return cls(
            id=uuid4(),
            data_producao=data_producao,
            quantidade_kg=quantidade_kg,
            unidade_processamento=unidade_processamento,
            destino=destino,
        )
