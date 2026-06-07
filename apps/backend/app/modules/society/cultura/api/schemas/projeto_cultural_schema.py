from __future__ import annotations

from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from apps.backend.app.modules.society.cultura.domain.enums import (
    NaturezaProjetoCultural,
    StatusProjetoCultural,
    TipoProjetoCultural,
)


class ProjetoCulturalCreate(BaseModel):
    titulo: str = Field(..., min_length=5)
    tipo: TipoProjetoCultural
    natureza: NaturezaProjetoCultural
    proponente_cpf_cnpj: str = Field(..., min_length=5)
    proponente_nome: str = Field(..., min_length=3)
    resumo: str = Field(..., min_length=10)
    valor_solicitado: Decimal = Field(..., gt=0)
    justificativa: str | None = None
    edital_id: UUID | None = None
    objetivos: list[str] = Field(default_factory=list)
    observacoes: str | None = None
    submeter: bool = True


class ProjetoCulturalUpdate(BaseModel):
    titulo: str | None = Field(default=None, min_length=5)
    tipo: TipoProjetoCultural | None = None
    natureza: NaturezaProjetoCultural | None = None
    resumo: str | None = None
    valor_solicitado: Decimal | None = Field(default=None, gt=0)
    justificativa: str | None = None
    objetivos: list[str] | None = None
    ativo: bool | None = None
    observacoes: str | None = None


class ProjetoAprovacaoRequest(BaseModel):
    valor_aprovado: Decimal = Field(..., gt=0)


class ProjetoExecucaoRequest(BaseModel):
    data: date


class ProjetoCulturalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_projeto: str
    titulo: str
    tipo: TipoProjetoCultural
    natureza: NaturezaProjetoCultural
    proponente_cpf_cnpj: str
    proponente_nome: str
    resumo: str
    valor_solicitado: Decimal
    valor_aprovado: Decimal | None = None
    data_submissao: date
    data_inicio: date | None = None
    data_fim: date | None = None
    status: StatusProjetoCultural
    edital_id: UUID | None = None
    justificativa: str | None = None
    objetivos: list[str]
    ativo: bool
    observacoes: str | None = None
