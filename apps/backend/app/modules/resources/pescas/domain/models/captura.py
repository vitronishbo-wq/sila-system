from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4


@dataclass
class Captura:
    id: UUID
    embarcacao_id: UUID
    licenca_id: UUID
    data_inicio: datetime
    data_fim: datetime
    zona_pesca_id: UUID
    especie_id: UUID
    quantidade_kg: Decimal
    arte_pesca_id: UUID
    quantidade_unidades: int | None = None
    profundidade: Decimal | None = None
    coordenadas_inicio: str | None = None
    coordenadas_fim: str | None = None
    condicoes_mar: str | None = None
    observacoes: str | None = None

    @classmethod
    def registrar(
        cls,
        *,
        embarcacao_id: UUID,
        licenca_id: UUID,
        zona_pesca_id: UUID,
        especie_id: UUID,
        quantidade_kg: Decimal,
        arte_pesca_id: UUID,
    ) -> Captura:
        now = datetime.utcnow()
        return cls(
            id=uuid4(),
            embarcacao_id=embarcacao_id,
            licenca_id=licenca_id,
            data_inicio=now,
            data_fim=now,
            zona_pesca_id=zona_pesca_id,
            especie_id=especie_id,
            quantidade_kg=quantidade_kg,
            arte_pesca_id=arte_pesca_id,
        )
