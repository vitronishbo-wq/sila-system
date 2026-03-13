from __future__ import annotations
from dataclasses import dataclass
from uuid import uuid4
from app.modules.tourism.domain.models import BaseTurismoModel

@dataclass
class Estrelas(BaseTurismoModel):

    @classmethod
    def criar(cls, *, nome: str) -> 'Estrelas':
        return cls(id=uuid4(), nome=nome.strip(), ativo=True)
