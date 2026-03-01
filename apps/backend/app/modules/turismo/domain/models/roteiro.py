from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4

from app.modules.turismo.domain.models import BaseTurismoModel


@dataclass
class Roteiro(BaseTurismoModel):
    @classmethod
    def criar(cls, *, nome: str) -> "Roteiro":
        return cls(id=uuid4(), nome=nome.strip(), ativo=True)
