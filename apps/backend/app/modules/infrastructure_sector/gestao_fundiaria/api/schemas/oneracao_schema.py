from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from app.modules.infrastructure_sector.gestao_fundiaria.domain.enums import StatusOneracao, TipoOneracao

class OneracaoCreate(BaseModel):
    imovel_inscricao: str
    tipo: TipoOneracao
    credor_nome: str
    valor: Decimal
    documento_credor: str | None = None
    data_vencimento: date | None = None
    descricao: str | None = None
    numero_oneracao: str | None = None

class OneracaoMotivoInput(BaseModel):
    motivo: str

class OneracaoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    numero_oneracao: str
    imovel_inscricao: str
    tipo: TipoOneracao
    credor_nome: str
    valor: Decimal
    data_registro: date
    status: StatusOneracao
    ativo: bool
    documento_credor: str | None = None
    moeda: str
    data_vencimento: date | None = None
    descricao: str | None = None
    data_atualizacao: date | None = None
    observacoes: str | None = None