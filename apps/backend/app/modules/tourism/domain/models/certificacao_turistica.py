from __future__ import annotations
from dataclasses import dataclass
from uuid import uuid4
from app.modules.tourism.domain.models import BaseTurismoModel

@dataclass
class CertificacaoTuristica(BaseTurismoModel):

    @classmethod
    def criar(cls, *, nome: str) -> 'CertificacaoTuristica':
        return cls(id=uuid4(), nome=nome.strip(), ativo=True)
