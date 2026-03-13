from __future__ import annotations
from dataclasses import dataclass
from uuid import UUID, uuid4

@dataclass
class EmbargoIndustrial:
    id: UUID
    nome: str
    ativo: bool = True

    @classmethod
    def criar(cls, *, nome: str) -> 'EmbargoIndustrial':
        return cls(id=uuid4(), nome=nome.strip(), ativo=True)