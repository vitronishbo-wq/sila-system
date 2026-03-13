from dataclasses import dataclass
from typing import Optional
from uuid import UUID, uuid4

@dataclass
class AreaReflorestada:
    id: UUID
    codigo: str
    descricao: str
    ativo: bool = True
    observacoes: Optional[str] = None

    @classmethod
    def criar(cls, *, codigo: str, descricao: str) -> 'AreaReflorestada':
        return cls(id=uuid4(), codigo=codigo, descricao=descricao)