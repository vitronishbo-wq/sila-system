from __future__ import annotations
from datetime import date, datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from app.modules.governance.cooperacao_internacional.domain.enums import NaturezaJuridica, StatusAcordo, TipoAcordo

class ParteAssinaturaInput(BaseModel):
    entidade_id: UUID
    tipo_entidade: str = Field(min_length=3, max_length=30)
    data_adesao: date
    assinante: str = Field(min_length=3, max_length=120)
    titulo_assinante: str = Field(min_length=2, max_length=80)

class AcordoCreate(BaseModel):
    titulo: str = Field(min_length=5, max_length=300)
    tipo: TipoAcordo
    natureza: NaturezaJuridica
    data_assinatura: date
    data_vigor: date | None = None
    prazo_anos: int | None = Field(default=None, ge=1, le=100)
    objeto: str = Field(min_length=8, max_length=4000)
    fundamento_legal: str | None = Field(default=None, max_length=500)
    texto_integral: str | None = None

class AcordoAssinarInput(BaseModel):
    partes: list[ParteAssinaturaInput]
    local_assinatura: str = Field(min_length=2, max_length=120)

class AcordoRatificarInput(BaseModel):
    data_ratificacao: date
    instrumento: str = Field(min_length=3, max_length=200)
    parte_id: UUID

class AcordoVigorInput(BaseModel):
    data_vigor: date

class AcordoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    numero_registro: str
    titulo: str
    tipo: TipoAcordo
    natureza: NaturezaJuridica
    status: StatusAcordo
    data_assinatura: date
    data_vigor: date | None
    prazo_anos: int | None
    objeto: str
    partes: list[dict]
    ratificacoes: list[dict]
    data_registro: datetime