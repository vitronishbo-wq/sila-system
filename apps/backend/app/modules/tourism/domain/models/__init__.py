from __future__ import annotations
from dataclasses import dataclass
from uuid import UUID

@dataclass
class BaseTurismoModel:
    id: UUID
    nome: str
    ativo: bool = True
__all__ = ['BaseTurismoModel']