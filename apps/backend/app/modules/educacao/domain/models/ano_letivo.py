from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from uuid import UUID


@dataclass
class AnoLetivo:
    id: UUID
    ano: int
    data_inicio: date
    data_fim: date
    ativo: bool = False

