from __future__ import annotations
from dataclasses import dataclass
from uuid import uuid4
from apps.backend.app.modules.tourism.domain.models import BaseTurismoModel

@dataclass
class OperadorTuristico(BaseTurismoModel):

    @classmethod
    def criar(cls, *, nome: str) -> 'OperadorTuristico':
        return cls(id=uuid4(), nome=nome.strip(), ativo=True)
