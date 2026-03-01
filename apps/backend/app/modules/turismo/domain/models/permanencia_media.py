from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4

from app.modules.turismo.domain.models import BaseTurismoModel


@dataclass
class PermanenciaMedia(BaseTurismoModel):
    @classmethod
    def criar(cls, *, nome: str) -> "PermanenciaMedia":
        return cls(id=uuid4(), nome=nome.strip(), ativo=True)
