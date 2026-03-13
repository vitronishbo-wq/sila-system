from __future__ import annotations
from dataclasses import dataclass
from uuid import uuid4
from apps.backend.app.modules.tourism.domain.models import BaseTurismoModel

@dataclass
class ReceitaTuristica(BaseTurismoModel):

    @classmethod
    def criar(cls, *, nome: str) -> 'ReceitaTuristica':
        return cls(id=uuid4(), nome=nome.strip(), ativo=True)
