from __future__ import annotations
from datetime import date
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from app.modules.economy.trade.external.domain.enums import StatusHabilitacao, TipoOperador, TipoPessoa

class OperadorLogisticoCreate(BaseModel):
    razao_social: str
    cnpj_cpf: str
    tipo_pessoa: TipoPessoa
    endereco: str
    numero: str
    bairro: str
    municipio: str
    provincia: str
    cep: str

class HabilitacaoOperadorInput(BaseModel):
    numero_radar: str
    data_habilitacao: date
    data_validade: date

class SuspensaoOperadorInput(BaseModel):
    data_suspensao: date
    motivo: str

class CancelamentoOperadorInput(BaseModel):
    data_cancelamento: date
    motivo: str

class OperadorLogisticoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    cadastro_radar: str
    tipo_operador: TipoOperador
    tipo_pessoa: TipoPessoa
    status: StatusHabilitacao
    razao_social: str
    nome_fantasia: str | None = None
    cnpj_cpf: str
    endereco: str
    numero: str
    complemento: str | None = None
    bairro: str
    municipio: str
    provincia: str
    cep: str
    pais: str
    telefone: str | None = None
    email: str | None = None
    site: str | None = None
    numero_licenca: str | None = None
    orgao_anuente: str | None = None
    data_habilitacao: date | None = None
    data_validade: date | None = None
    data_suspensao: date | None = None
    data_cancelamento: date | None = None
    motivo_cancelamento: str | None = None
    observacoes: str | None = None