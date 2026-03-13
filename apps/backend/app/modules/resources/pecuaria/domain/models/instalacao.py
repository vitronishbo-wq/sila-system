from dataclasses import dataclass
from uuid import UUID, uuid4
from app.modules.resources.pecuaria.domain.enums import TipoInstalacao

@dataclass
class Instalacao:
    id: UUID
    propriedade_id: UUID
    tipo: TipoInstalacao
    descricao: str

    @classmethod
    def criar(cls, *, propriedade_id: UUID, tipo: TipoInstalacao, descricao: str) -> 'Instalacao':
        return cls(id=uuid4(), propriedade_id=propriedade_id, tipo=tipo, descricao=descricao)