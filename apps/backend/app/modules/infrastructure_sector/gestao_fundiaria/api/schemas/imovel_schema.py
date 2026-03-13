from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.domain.enums import NaturezaImovel, RegimePropriedade, SituacaoDominial, TipoImovel

class ImovelCreate(BaseModel):
    tipo: TipoImovel
    natureza: NaturezaImovel
    area_total: Decimal
    endereco: str
    bairro: str
    municipio: str
    provincia: str
    inscricao_imobiliaria: str | None = None

class ImovelAreaInput(BaseModel):
    area_total: Decimal

class ImovelProprietarioInput(BaseModel):
    proprietario_id: UUID

class ImovelSituacaoInput(BaseModel):
    situacao: SituacaoDominial

class ImovelMatriculaInput(BaseModel):
    matricula_id: UUID

class ImovelMotivoInput(BaseModel):
    motivo: str

class ImovelResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    inscricao_imobiliaria: str
    tipo: TipoImovel
    natureza: NaturezaImovel
    regime: RegimePropriedade
    situacao: SituacaoDominial
    area_total: Decimal
    endereco: str
    bairro: str
    municipio: str
    provincia: str
    data_cadastro: date
    area_privativa: Decimal | None = None
    area_construida: Decimal | None = None
    area_terreno: Decimal | None = None
    cep: str | None = None
    coordenadas_lat: Decimal | None = None
    coordenadas_long: Decimal | None = None
    matricula_id: UUID | None = None
    proprietario_atual_id: UUID | None = None
    data_atualizacao: date | None = None
    ativo: bool
    observacoes: str | None = None