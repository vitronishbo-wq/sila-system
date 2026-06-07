from __future__ import annotations

from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from apps.backend.app.modules.economy.trade.external.domain.enums import (
    RegimeImportacao,
    StatusHabilitacao,
    TipoOperador,
    TipoPessoa,
)


class ImportadorCreate(BaseModel):
    razao_social: str
    cnpj_cpf: str
    tipo_pessoa: TipoPessoa
    endereco: str
    numero: str
    bairro: str
    municipio: str
    provincia: str
    cep: str
    regimes_autorizados: list[RegimeImportacao]


class HabilitacaoImportadorInput(BaseModel):
    numero_radar: str
    data_habilitacao: date
    data_validade: date


class SuspensaoImportadorInput(BaseModel):
    data_suspensao: date
    motivo: str


class CancelamentoImportadorInput(BaseModel):
    data_cancelamento: date
    motivo: str


class ProdutoImportadorInput(BaseModel):
    produto: str


class PaisOrigemInput(BaseModel):
    pais: str


class ImportadorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    cadastro_radar: str
    tipo_operador: TipoOperador
    tipo_pessoa: TipoPessoa
    status: StatusHabilitacao
    razao_social: str
    nome_fantasia: str | None = None
    cnpj_cpf: str
    inscricao_estadual: str | None = None
    inscricao_municipal: str | None = None
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
    representante_nome: str | None = None
    representante_cpf: str | None = None
    representante_cargo: str | None = None
    responsavel_nome: str | None = None
    responsavel_cpf: str | None = None
    responsavel_registro: str | None = None
    data_habilitacao: date | None = None
    data_validade: date | None = None
    data_suspensao: date | None = None
    data_cancelamento: date | None = None
    motivo_cancelamento: str | None = None
    regimes_autorizados: list[RegimeImportacao]
    produtos_principais: list[str] | None = None
    paises_origem: list[str] | None = None
    banco_principal: str | None = None
    conta_corrente: str | None = None
    swift_code: str | None = None
    limite_credito: Decimal | None = None
    observacoes: str | None = None
