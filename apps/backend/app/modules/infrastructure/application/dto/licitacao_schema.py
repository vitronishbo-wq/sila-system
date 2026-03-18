from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from apps.backend.app.modules.infrastructure.domain.enums import StatusLicitacao, TipoLicitacao

class LicitacaoCreate(BaseModel):
    objeto: str
    tipo: TipoLicitacao
    obra_id: UUID
    orgao_responsavel_id: UUID
    valor_estimado: Decimal
    data_publicacao_edital: date
    data_entrega_propostas: date
    numero_licitacao: str | None = None

class LicitacaoAberturaInput(BaseModel):
    data_abertura: date

class LicitacaoAdjudicacaoInput(BaseModel):
    vencedor_id: UUID
    valor_adjudicado: Decimal

class LicitacaoHomologacaoInput(BaseModel):
    data_homologacao: date | None = None

class LicitacaoMotivoInput(BaseModel):
    motivo: str

class LicitacaoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    numero_licitacao: str
    objeto: str
    tipo: TipoLicitacao
    status: StatusLicitacao
    obra_id: UUID
    orgao_responsavel_id: UUID
    valor_estimado: Decimal
    data_publicacao_edital: date
    data_entrega_propostas: date
    data_cadastro: date
    data_abertura: date | None = None
    vencedor_id: UUID | None = None
    valor_adjudicado: Decimal | None = None
    data_homologacao: date | None = None
    data_atualizacao: date | None = None
    observacoes: str | None = None