from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from uuid import UUID, uuid4

@dataclass
class Especie:
    id: UUID
    nome_comum: str
    nome_cientifico: str
    codigo_fao: str
    ameacada: bool = False
    observacoes: Optional[str] = None

    @classmethod
    def cadastrar(cls, *, nome_comum: str, nome_cientifico: str, codigo_fao: str) -> 'Especie':
        return cls(id=uuid4(), nome_comum=nome_comum, nome_cientifico=nome_cientifico, codigo_fao=codigo_fao)