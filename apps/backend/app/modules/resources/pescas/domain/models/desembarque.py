from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4


@dataclass
class Desembarque:
    id: UUID
    captura_id: UUID
    porto_desembarque: str
    data_desembarque: datetime
    quantidade_kg: Decimal
    inspecao_aprovada: bool = False
    observacoes: str | None = None

    @classmethod
    def registrar(
        cls, *, captura_id: UUID, porto_desembarque: str, quantidade_kg: Decimal
    ) -> Desembarque:
        return cls(
            id=uuid4(),
            captura_id=captura_id,
            porto_desembarque=porto_desembarque,
            data_desembarque=datetime.utcnow(),
            quantidade_kg=quantidade_kg,
        )
