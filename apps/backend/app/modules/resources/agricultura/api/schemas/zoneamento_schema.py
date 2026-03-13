from __future__ import annotations
from datetime import date
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from apps.backend.app.modules.resources.agricultura.domain.enums import AptidaoSolo, StatusCadastroAmbiental, StatusZoneamento, TipoZonaAgricola

class ZoneamentoCreate(BaseModel):
    codigo_propriedade: str
    zona: TipoZonaAgricola
    aptidao_solo: AptidaoSolo
    area_zoneada_ha: float
    culturas_recomendadas: list[str] | None = None
    restricoes: list[str] | None = None
    validade_ate: date | None = None
    observacoes: str | None = None

class ZoneamentoRevogacaoInput(BaseModel):
    motivo: str

class CadastroAmbientalCreate(BaseModel):
    reserva_legal_percentual: float
    app_percentual: float
    area_protecao_ha: float
    numero_processo: str | None = None

class CadastroAmbientalValidacaoInput(BaseModel):
    numero_processo: str

class CadastroAmbientalPendenciaInput(BaseModel):
    pendencia: str

class ZoneamentoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_zoneamento: str
    codigo_propriedade: str
    zona: TipoZonaAgricola
    aptidao_solo: AptidaoSolo
    area_zoneada_ha: float
    status: StatusZoneamento
    data_zoneamento: date
    culturas_recomendadas: list[str] | None = None
    restricoes: list[str] | None = None
    validade_ate: date | None = None
    observacoes: str | None = None

class CadastroAmbientalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_cadastro_ambiental: str
    codigo_zoneamento: str
    codigo_propriedade: str
    reserva_legal_percentual: float
    app_percentual: float
    area_protecao_ha: float
    status: StatusCadastroAmbiental
    data_registro: date
    numero_processo: str | None = None
    data_validacao: date | None = None
    pendencias: list[str] | None = None