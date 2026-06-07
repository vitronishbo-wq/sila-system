from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass
class TipoEmbarcacao:
    id: UUID
    codigo: str
    descricao: str
    ativo: bool = True
    observacoes: str | None = None

    @classmethod
    def criar(cls, *, codigo: str, descricao: str) -> TipoEmbarcacao:
        return cls(id=uuid4(), codigo=codigo, descricao=descricao)
