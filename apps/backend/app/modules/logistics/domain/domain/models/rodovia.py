from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Any
from uuid import UUID
from app.modules.logistics.domain.enums import ClassificacaoVia, TipoPavimento

@dataclass
class Rodovia:
    id: UUID
    codigo: str
    nome: str
    classificacao: ClassificacaoVia
    tipo_pavimento: TipoPavimento
    extensao_km: Decimal
    origem: str
    destino: str
    concessionaria_id: UUID | None = None
    data_inauguracao: date | None = None
    ultima_reforma: date | None = None
    numero_pistas: int | None = None
    numero_faixas: int | None = None
    velocidade_maxima: int | None = None
    pedagio: bool = False
    valor_pedagio: Decimal | None = None
    coordenadas_geograficas: list[dict[str, Any]] | None = None
    observacoes: str | None = None
