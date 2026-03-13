from __future__ import annotations
from datetime import date
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from apps.backend.app.modules.economy.trade.external.domain.enums import StatusHabilitacao, TipoOperador, TipoPessoa

class HabilitacaoCreateBase(BaseModel):
    tipo_pessoa: TipoPessoa
    razao_social: str
    cnpj_cpf: str
    numero_processo: str
    data_solicitacao: date

class HabilitacaoAprovacaoInput(BaseModel):
    numero_radar: str
    data_analise: date
    data_validade: date

class HabilitacaoRejeicaoInput(BaseModel):
    data_analise: date
    motivo: str

class HabilitacaoResponseBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    tipo_operador: TipoOperador
    tipo_pessoa: TipoPessoa
    status: StatusHabilitacao
    razao_social: str
    cnpj_cpf: str
    numero_processo: str
    data_solicitacao: date
    data_analise: date | None = None
    data_validade: date | None = None
    numero_radar: str | None = None
    motivo: str | None = None
    observacoes: str | None = None