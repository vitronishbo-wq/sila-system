from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID, uuid4


@dataclass
class Quota:
    id: UUID
    especie_id: UUID
    zona_pesca_id: UUID
    ano: int
    limite_kg: Decimal
    utilizado_kg: Decimal
    observacoes: str | None = None

    @classmethod
    def criar(cls, *, especie_id: UUID, zona_pesca_id: UUID, ano: int, limite_kg: Decimal) -> Quota:
        return cls(
            id=uuid4(),
            especie_id=especie_id,
            zona_pesca_id=zona_pesca_id,
            ano=ano,
            limite_kg=limite_kg,
            utilizado_kg=Decimal("0"),
        )

    def registrar_consumo(self, quantidade_kg: Decimal) -> None:
        self.utilizado_kg += quantidade_kg
