from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from uuid import UUID


class Turno(StrEnum):
    MANHA = "manha"
    TARDE = "tarde"
    NOITE = "noite"
    INTEGRAL = "integral"


@dataclass
class Turma:
    id: UUID
    escola_id: UUID
    ano_letivo_id: UUID
    codigo: str
    classe: str
    turno: Turno
    capacidade: int
    ativa: bool = True
