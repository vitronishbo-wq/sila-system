from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import StatusParcelamento, TipoParcelamento

class ParcelamentoCreate(BaseModel):
    nome: str
    tipo: TipoParcelamento
    plano_diretor_id: UUID
    zoneamento_id: UUID
    provincia: str
    area_total: Decimal
    quantidade_unidades_prevista: int
    municipio: str | None = None
    area_publica_prevista: Decimal | None = None
    area_sistema_viario_prevista: Decimal | None = None
    codigo_parcelamento: str | None = None

class ParcelamentoConclusaoInput(BaseModel):
    quantidade_unidades_resultante: int

class ParcelamentoMotivoInput(BaseModel):
    motivo: str

class ParcelamentoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_parcelamento: str
    nome: str
    tipo: TipoParcelamento
    status: StatusParcelamento
    plano_diretor_id: UUID
    zoneamento_id: UUID
    provincia: str
    area_total: Decimal
    quantidade_unidades_prevista: int
    municipio: str | None = None
    area_publica_prevista: Decimal | None = None
    area_sistema_viario_prevista: Decimal | None = None
    quantidade_unidades_resultante: int | None = None
    data_cadastro: date
    data_atualizacao: date | None = None
    observacoes: str | None = None