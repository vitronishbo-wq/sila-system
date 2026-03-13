from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from app.modules.infrastructure_sector.gestao_fundiaria.domain.enums import TipoPessoa, TipoTitularidade

class ProprietarioCreate(BaseModel):
    nome: str
    documento: str
    tipo_pessoa: TipoPessoa
    tipo_titularidade: TipoTitularidade
    percentual_titularidade: Decimal | None = None
    email: str | None = None
    telefone: str | None = None
    endereco: str | None = None

class ProprietarioContatoInput(BaseModel):
    email: str | None = None
    telefone: str | None = None
    endereco: str | None = None

class ProprietarioTitularidadeInput(BaseModel):
    tipo_titularidade: TipoTitularidade
    percentual_titularidade: Decimal | None = None

class ProprietarioMotivoInput(BaseModel):
    motivo: str

class ProprietarioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    numero_cadastro: str
    nome: str
    documento: str
    tipo_pessoa: TipoPessoa
    tipo_titularidade: TipoTitularidade
    data_cadastro: date
    ativo: bool
    percentual_titularidade: Decimal | None = None
    email: str | None = None
    telefone: str | None = None
    endereco: str | None = None
    data_atualizacao: date | None = None
    observacoes: str | None = None