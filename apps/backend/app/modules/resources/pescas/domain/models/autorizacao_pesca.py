from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from uuid import UUID, uuid4

@dataclass
class AutorizacaoPesca:
    id: UUID
    codigo: str
    descricao: str
    ativo: bool = True
    observacoes: Optional[str] = None

    @classmethod
    def criar(cls, *, codigo: str, descricao: str) -> 'AutorizacaoPesca':
        return cls(id=uuid4(), codigo=codigo, descricao=descricao)