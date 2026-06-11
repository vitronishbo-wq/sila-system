
from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from uuid import UUID, uuid4


class Turno(StrEnum):
    MANHA = "manha"
    TARDE = "tarde"
    NOITE = "noite"
    INTEGRAL = "integral"


@dataclass
class Turma:
    id: UUID = field(default_factory=uuid4)
    escola_id: UUID
    ano_letivo_id: UUID
    codigo: str
    classe: str
    turno: Turno
    capacidade: int
    territory_id: UUID  # Princípio 8: Herança explícita para governança direta
    created_by: UUID  # Princípio 8
    managed_by: UUID  # Princípio 8
    ativa: bool = True
