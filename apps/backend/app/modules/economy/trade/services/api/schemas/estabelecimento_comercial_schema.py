from __future__ import annotations
from datetime import date, datetime
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from apps.backend.app.modules.economy.trade.services.domain.enums import PorteComercial, RamoComercial, StatusComercial, TipoEstabelecimentoComercial, TipoRegimeTributario

class EstabelecimentoComercialCreate(BaseModel):
    cnpj: str
    razao_social: str
    tipo: TipoEstabelecimentoComercial
    ramo: RamoComercial
    porte: PorteComercial
    regime_tributario: TipoRegimeTributario
    cnae_principal: str
    data_abertura: date
    endereco: str
    numero: str
    bairro: str
    municipio: str
    provincia: str
    cep: str

class DataInput(BaseModel):
    data: date

class MotivoInput(BaseModel):
    motivo: str

class RamoInput(BaseModel):
    ramo: RamoComercial

class PorteInput(BaseModel):
    porte: PorteComercial

class EncerramentoInput(BaseModel):
    data_encerramento: date
    motivo: str

class EstabelecimentoComercialResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    cnpj: str
    razao_social: str
    tipo: TipoEstabelecimentoComercial
    ramo: RamoComercial
    porte: PorteComercial
    regime_tributario: TipoRegimeTributario
    cnae_principal: str
    data_abertura: date
    endereco: str
    numero: str
    bairro: str
    municipio: str
    provincia: str
    cep: str
    status: StatusComercial
    inscricao_estadual: str | None = None
    inscricao_municipal: str | None = None
    nome_fantasia: str | None = None
    cnaes_secundarios: list[str] | None = None
    data_inicio_atividades: date | None = None
    data_encerramento: date | None = None
    complemento: str | None = None
    coordenadas_lat: Decimal | None = None
    coordenadas_long: Decimal | None = None
    telefone: str | None = None
    celular: str | None = None
    email: str | None = None
    site: str | None = None
    redes_sociais: dict | None = None
    horario_funcionamento: dict | None = None
    dias_funcionamento: list[str] | None = None
    area_m2: Decimal | None = None
    numero_funcionarios: int | None = None
    faturamento_medio_mensal: Decimal | None = None
    matriz_id: UUID | None = None
    franquia_id: UUID | None = None
    grupo_economico_id: UUID | None = None
    proprietario_id: UUID | None = None
    proprietario_tipo: str | None = None
    alvara_id: UUID | None = None
    licenca_sanitaria_id: UUID | None = None
    licenca_ambiental_id: UUID | None = None
    certificacoes: list[UUID] | None = None
    created_at: datetime
    updated_at: datetime
    audit_log: list[str] = Field(default_factory=list)
    observacoes: str | None = None