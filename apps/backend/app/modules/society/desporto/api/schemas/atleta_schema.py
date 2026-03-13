from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from app.modules.society.desporto.domain.enums import ModalidadeDesportiva, PePreferencial, PosicaoAtleta, StatusAtleta, TipoAtleta

class AtletaCreate(BaseModel):
    nome: str = Field(..., min_length=3)
    data_nascimento: date
    naturalidade: str
    nacionalidade: str = 'Angolana'
    tipo: TipoAtleta
    modalidades: list[ModalidadeDesportiva] = Field(..., min_length=1)
    citizen_id: UUID | None = None
    posicoes: list[PosicaoAtleta] | None = None
    pe_preferencial: PePreferencial | None = None
    altura_cm: int | None = Field(default=None, gt=0)
    peso_kg: Decimal | None = Field(default=None, gt=0)
    clube_atual_id: UUID | None = None
    numero_camisola: int | None = None
    ultimo_exame_id: UUID | None = None
    observacoes: str | None = None

class AtletaUpdate(BaseModel):
    nome: str | None = Field(default=None, min_length=3)
    tipo: TipoAtleta | None = None
    modalidades: list[ModalidadeDesportiva] | None = None
    posicoes: list[PosicaoAtleta] | None = None
    pe_preferencial: PePreferencial | None = None
    altura_cm: int | None = Field(default=None, gt=0)
    peso_kg: Decimal | None = Field(default=None, gt=0)
    clube_atual_id: UUID | None = None
    numero_camisola: int | None = None
    status: StatusAtleta | None = None
    ultimo_exame_id: UUID | None = None
    ativo: bool | None = None
    observacoes: str | None = None

class AtletaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    numero_registro: str
    nome: str
    data_nascimento: date
    naturalidade: str
    nacionalidade: str
    tipo: TipoAtleta
    modalidades: list[ModalidadeDesportiva]
    data_cadastro: date
    status: StatusAtleta
    posicoes: list[PosicaoAtleta] | None = None
    pe_preferencial: PePreferencial | None = None
    altura_cm: int | None = None
    peso_kg: Decimal | None = None
    clube_atual_id: UUID | None = None
    numero_camisola: int | None = None
    citizen_id: UUID | None = None
    ultimo_exame_id: UUID | None = None
    observacoes: str | None = None
    ativo: bool