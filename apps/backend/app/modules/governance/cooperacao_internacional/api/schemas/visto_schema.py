from __future__ import annotations
from datetime import date, datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from app.modules.governance.cooperacao_internacional.domain.enums import CategoriaVisto, StatusVisto, TipoVisto

class VistoCreate(BaseModel):
    tipo: TipoVisto
    categoria: CategoriaVisto
    solicitante_cpf: str = Field(min_length=5, max_length=20)
    solicitante_nome: str = Field(min_length=3, max_length=200)
    solicitante_passaporte: str = Field(min_length=5, max_length=30)
    pais_origem_id: UUID
    pais_destino_id: UUID
    data_entrada_prevista: date
    data_saida_prevista: date
    objetivo_viagem: str = Field(min_length=5, max_length=1000)
    consulato_emissor_id: UUID

class VistoAnaliseInput(BaseModel):
    analista: str = Field(min_length=3, max_length=120)
    resultado: str = Field(min_length=2, max_length=120)
    justificativa: str | None = Field(default=None, max_length=1000)

class VistoAprovarInput(BaseModel):
    autoridade: str = Field(min_length=3, max_length=120)
    validade_dias: int = Field(default=90, ge=1, le=3650)

class VistoNegarInput(BaseModel):
    motivo: str = Field(min_length=3, max_length=1000)

class VistoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    numero_processo: str
    tipo: TipoVisto
    categoria: CategoriaVisto
    solicitante_cpf: str
    solicitante_nome: str
    solicitante_passaporte: str
    pais_origem_id: UUID
    pais_destino_id: UUID
    data_solicitacao: datetime
    data_entrada_prevista: date
    data_saida_prevista: date
    objetivo_viagem: str
    consulato_emissor_id: UUID
    status: StatusVisto
    data_emissao: date | None
    data_validade: date | None
    numero_visto: str | None
    historico_analise: list[dict]