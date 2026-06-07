from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4


@dataclass
class Armador:
    id: UUID
    nome: str
    nif: str
    data_registro: date
    ativo: bool = True
    telefone: str | None = None
    email: str | None = None
    observacoes: str | None = None

    @classmethod
    def cadastrar(cls, *, nome: str, nif: str) -> Armador:
        return cls(id=uuid4(), nome=nome, nif=nif, data_registro=date.today())
