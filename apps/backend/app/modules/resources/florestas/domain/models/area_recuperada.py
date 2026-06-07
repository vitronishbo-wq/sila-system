from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass
class AreaRecuperada:
    id: UUID
    codigo: str
    descricao: str
    ativo: bool = True
    observacoes: str | None = None

    @classmethod
    def criar(cls, *, codigo: str, descricao: str) -> "AreaRecuperada":
        return cls(id=uuid4(), codigo=codigo, descricao=descricao)
