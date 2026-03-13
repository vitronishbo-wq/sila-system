from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import Optional
from uuid import UUID, uuid4
from apps.backend.app.modules.resources.pescas.domain.enums import PeriodoDefesoTipo

@dataclass
class Defeso:
    id: UUID
    periodo: PeriodoDefesoTipo
    especie_id: UUID
    data_inicio: date
    data_fim: date
    ativo: bool = True
    observacoes: Optional[str] = None

    @classmethod
    def criar(cls, *, periodo: PeriodoDefesoTipo, especie_id: UUID, data_inicio: date, data_fim: date) -> 'Defeso':
        return cls(id=uuid4(), periodo=periodo, especie_id=especie_id, data_inicio=data_inicio, data_fim=data_fim)