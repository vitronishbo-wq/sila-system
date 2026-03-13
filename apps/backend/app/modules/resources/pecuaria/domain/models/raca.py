from __future__ import annotations
from dataclasses import dataclass
from uuid import UUID, uuid4
from apps.backend.app.modules.resources.pecuaria.domain.enums import TipoAnimal

@dataclass
class Raca:
    id: UUID
    nome: str
    tipo_animal: TipoAnimal
    aptidao: str | None = None

    @classmethod
    def criar(cls, *, nome: str, tipo_animal: TipoAnimal, aptidao: str | None=None) -> 'Raca':
        return cls(id=uuid4(), nome=nome, tipo_animal=tipo_animal, aptidao=aptidao)