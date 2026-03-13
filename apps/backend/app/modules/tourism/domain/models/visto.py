from __future__ import annotations
from dataclasses import dataclass
from uuid import uuid4
from apps.backend.app.modules.tourism.domain.models import BaseTurismoModel

@dataclass
class Visto(BaseTurismoModel):

    @classmethod
    def criar(cls, *, nome: str) -> 'Visto':
        return cls(id=uuid4(), nome=nome.strip(), ativo=True)
