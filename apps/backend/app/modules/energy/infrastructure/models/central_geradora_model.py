from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID
from app.modules.energy.domain.enums import FonteEnergia, StatusInfraEnergia

@dataclass
class CentralGeradoraModel:
    id: UUID
    nome: str
    tipo: FonteEnergia
    capacidade_instalada_mw: Decimal
    municipio: str
    provincia: str
    status: StatusInfraEnergia
    data_inicio_construcao: date | None = None
    data_inicio_operacao: date | None = None
