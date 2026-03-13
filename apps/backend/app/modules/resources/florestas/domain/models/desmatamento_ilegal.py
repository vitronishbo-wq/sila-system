from dataclasses import dataclass
from typing import Optional
from uuid import UUID, uuid4

@dataclass
class DesmatamentoIlegal:
    id: UUID
    codigo: str
    descricao: str
    ativo: bool = True
    observacoes: Optional[str] = None

    @classmethod
    def criar(cls, *, codigo: str, descricao: str) -> 'DesmatamentoIlegal':
        return cls(id=uuid4(), codigo=codigo, descricao=descricao)