from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.enums import StatusAssinante, TipoPlano, TipoServico

class AssinanteCreate(BaseModel):
    operadora_id: UUID
    tipo_plano: TipoPlano
    servico_principal: TipoServico
    municipio: str
    provincia: str
    nome: str | None = None
    citizen_id: UUID | None = None
    telefone_contato: str | None = None
    email_contato: str | None = None
    contrato_numero: str | None = None
    valor_mensal: Decimal | None = Field(default=None, ge=0)
    observacoes: str | None = None

class AssinanteStatusUpdate(BaseModel):
    status: StatusAssinante

class AssinanteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_assinante: str
    operadora_id: UUID
    tipo_plano: TipoPlano
    servico_principal: TipoServico
    data_adesao: date
    status: StatusAssinante
    municipio: str
    provincia: str
    nome: str | None = None
    citizen_id: UUID | None = None
    contrato_numero: str | None = None
    valor_mensal: float | None = None
    ativo: bool