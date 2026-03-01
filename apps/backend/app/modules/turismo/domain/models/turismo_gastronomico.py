from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4

from app.modules.turismo.domain.models import BaseTurismoModel


@dataclass
class TurismoGastronomico(BaseTurismoModel):
    @classmethod
    def criar(cls, *, nome: str) -> "TurismoGastronomico":
        return cls(id=uuid4(), nome=nome.strip(), ativo=True)
