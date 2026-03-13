from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID
from app.modules.energy.domain.enums import ClasseTensao, StatusInfraEnergia

@dataclass
class SubestacaoModel:
    id: UUID
    nome: str
    tensao_nominal_kv: Decimal
    classe_tensao: ClasseTensao
    municipio: str
    provincia: str
    status: StatusInfraEnergia
    data_inicio_construcao: date | None = None
    data_inicio_operacao: date | None = None
