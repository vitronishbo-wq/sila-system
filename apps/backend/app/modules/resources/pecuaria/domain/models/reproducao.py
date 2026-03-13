from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4

@dataclass
class Reproducao:
    id: UUID
    femea_id: UUID
    macho_id: UUID | None
    data_evento: date
    metodo: str

    @classmethod
    def registrar(cls, *, femea_id: UUID, metodo: str, data_evento: date, macho_id: UUID | None=None) -> 'Reproducao':
        return cls(id=uuid4(), femea_id=femea_id, macho_id=macho_id, data_evento=data_evento, metodo=metodo)