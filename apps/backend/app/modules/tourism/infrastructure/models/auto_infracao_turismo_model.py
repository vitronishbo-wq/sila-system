from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass
class AutoInfracaoTurismoModel:
    id: UUID
    nome: str
