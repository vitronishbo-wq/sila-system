from __future__ import annotations
from datetime import datetime
from typing import Any
from uuid import UUID
from pydantic import BaseModel, Field, model_validator
from app.modules.infrastructure_sector.meteorologia.domain.enums import ObservationType

class ObservacaoCreateSchema(BaseModel):
    estacao_id: UUID = Field(..., description='ID da estacao meteorologica')
    data_observacao: datetime | None = Field(None, description='Data/hora da observacao')
    temperatura: float | None = Field(None, ge=-50, le=60)
    humidade: float | None = Field(None, ge=0, le=100)
    pressao: float | None = Field(None, ge=870, le=1084)
    velocidade_vento: float | None = Field(None, ge=0, le=300)
    direcao_vento: float | None = Field(None, ge=0, le=360)
    precipitacao: float | None = Field(None, ge=0)
    radiacao_solar: float | None = Field(None, ge=0)
    tipo: ObservationType = ObservationType.SURFACE
    metadata: dict = Field(default_factory=dict)

    @model_validator(mode='after')
    def validate_payload(self) -> 'ObservacaoCreateSchema':
        if all((valor is None for valor in (self.temperatura, self.humidade, self.pressao, self.velocidade_vento, self.direcao_vento, self.precipitacao, self.radiacao_solar))):
            raise ValueError('Informe ao menos uma leitura meteorologica')
        return self
    model_config = {'json_schema_extra': {'example': {'estacao_id': '550e8400-e29b-41d4-a716-446655440000', 'temperatura': 32.5, 'humidade': 45.0, 'pressao': 1012.2, 'velocidade_vento': 15.3, 'direcao_vento': 180.0, 'tipo': 'SURFACE'}}}

class ObservacaoResponseSchema(BaseModel):
    id: UUID
    estacao_id: UUID
    data_observacao: datetime
    leituras: dict[str, Any]
    tipo: str
    qualidade_dados: str
    alertas: list[dict[str, Any]]
    has_alerts: bool
    created_at: datetime

class AlertaResponseSchema(BaseModel):
    tipo: str
    severidade: str
    mensagem: str
    valor: float
    limite: float