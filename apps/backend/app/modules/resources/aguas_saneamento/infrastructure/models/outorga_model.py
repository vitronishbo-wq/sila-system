from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID
from app.modules.resources.aguas_saneamento.domain.enums import StatusOutorga, TipoCaptacao, TipoOutorga, TipoUso

@dataclass
class OutorgaModel:
    id: UUID
    numero_outorga: str
    tipo: TipoOutorga
    status: StatusOutorga
    requerente_id: UUID
    requerente_tipo: str
    corpo_hidrico_id: UUID
    tipo_captacao: TipoCaptacao | None
    vazao: Decimal
    unidade_vazao: str
    tempo_captacao: int | None
    periodo_captacao: str | None
    finalidade_uso: TipoUso
    data_requerimento: date