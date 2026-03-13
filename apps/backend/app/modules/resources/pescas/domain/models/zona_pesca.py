from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from uuid import UUID, uuid4

@dataclass
class ZonaPesca:
    id: UUID
    codigo: str
    nome: str
    area_km2: float
    ativa: bool = True
    observacoes: Optional[str] = None

    @classmethod
    def criar(cls, *, codigo: str, nome: str, area_km2: float) -> 'ZonaPesca':
        return cls(id=uuid4(), codigo=codigo, nome=nome, area_km2=area_km2)