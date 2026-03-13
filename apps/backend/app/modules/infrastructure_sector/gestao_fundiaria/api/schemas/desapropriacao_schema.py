from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from app.modules.infrastructure_sector.gestao_fundiaria.domain.enums import StatusDesapropriacao, TipoDesapropriacao

class DesapropriacaoCreate(BaseModel):
    imovel_inscricao: str
    tipo: TipoDesapropriacao
    ente_publico: str
    finalidade: str
    valor_indenizacao: Decimal
    numero_processo: str | None = None

class DesapropriacaoDecretoInput(BaseModel):
    data_decreto: date

class DesapropriacaoPagamentoInput(BaseModel):
    data_pagamento: date | None = None

class DesapropriacaoMotivoInput(BaseModel):
    motivo: str

class DesapropriacaoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    numero_processo: str
    imovel_inscricao: str
    tipo: TipoDesapropriacao
    ente_publico: str
    finalidade: str
    valor_indenizacao: Decimal
    data_inicio: date
    status: StatusDesapropriacao
    ativo: bool
    data_decreto: date | None = None
    data_pagamento: date | None = None
    data_atualizacao: date | None = None
    observacoes: str | None = None