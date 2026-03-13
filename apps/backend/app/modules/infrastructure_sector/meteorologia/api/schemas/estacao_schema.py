from __future__ import annotations
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field
from apps.backend.app.modules.infrastructure_sector.meteorologia.domain.enums import StationStatus

class EstacaoCreateSchema(BaseModel):
    codigo: str = Field(..., min_length=2, max_length=30, description='Codigo unico da estacao')
    nome: str = Field(..., min_length=3, max_length=200, description='Nome da estacao')
    latitude: float = Field(..., ge=-90, le=90, description='Latitude em graus')
    longitude: float = Field(..., ge=-180, le=180, description='Longitude em graus')
    altitude: float | None = Field(None, ge=-500, le=9000, description='Altitude em metros')
    municipio: str | None = Field(None, max_length=120)
    provincia: str | None = Field(None, max_length=120)
    metadata: dict = Field(default_factory=dict)
    model_config = {'json_schema_extra': {'example': {'codigo': 'ST-LDA-001', 'nome': 'Estacao Meteorologica Luanda Sul', 'latitude': -8.8383, 'longitude': 13.2344, 'altitude': 74.0, 'municipio': 'Luanda', 'provincia': 'Luanda', 'metadata': {'fonte': 'iot-gateway-01'}}}}

class EstacaoUpdateSchema(BaseModel):
    nome: str | None = Field(None, min_length=3, max_length=200)
    latitude: float | None = Field(None, ge=-90, le=90)
    longitude: float | None = Field(None, ge=-180, le=180)
    altitude: float | None = Field(None, ge=-500, le=9000)
    municipio: str | None = Field(None, max_length=120)
    provincia: str | None = Field(None, max_length=120)
    status: StationStatus | None = None
    metadata: dict | None = None

class EstacaoResponseSchema(BaseModel):
    id: UUID
    codigo: str
    nome: str
    latitude: float
    longitude: float
    altitude: float | None
    status: StationStatus
    municipio: str | None
    provincia: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    model_config = {'from_attributes': True}