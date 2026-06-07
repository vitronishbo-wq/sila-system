from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class RastreabilidadePesca:
    id: UUID
    lote_codigo: str
    origem_captura_id: UUID
    etapa: str
    data_evento: datetime
    operador: str
    observacoes: str | None = None

    @classmethod
    def registrar(
        cls, *, lote_codigo: str, origem_captura_id: UUID, etapa: str, operador: str
    ) -> RastreabilidadePesca:
        return cls(
            id=uuid4(),
            lote_codigo=lote_codigo,
            origem_captura_id=origem_captura_id,
            etapa=etapa,
            data_evento=datetime.utcnow(),
            operador=operador,
        )
