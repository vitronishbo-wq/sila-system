from __future__ import annotations
from dataclasses import dataclass, field
from datetime import UTC, datetime

@dataclass(slots=True)
class TimeSeries:
    metrica_id: int
    timestamp: datetime
    valor: float
    id: int | None = None
    dimensao_1: str | None = None
    dimensao_2: str | None = None
    dimensao_3: str | None = None
    origem: str | None = None
    criado_em: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def get_periodo(cls, data: datetime, periodicidade: str) -> datetime:
        if periodicidade == 'diaria':
            return data.replace(hour=0, minute=0, second=0, microsecond=0)
        if periodicidade == 'mensal':
            return data.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if periodicidade == 'anual':
            return data.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        return data