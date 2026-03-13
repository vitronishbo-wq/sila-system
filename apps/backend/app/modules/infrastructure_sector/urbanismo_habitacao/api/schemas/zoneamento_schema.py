from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import StatusZoneamento, TipoZona, UsoPermitido

class ZoneamentoCreate(BaseModel):
    nome: str
    tipo_zona: TipoZona
    plano_diretor_id: UUID
    provincia: str
    usos_permitidos: list[UsoPermitido]
    municipio: str | None = None
    codigo_zoneamento: str | None = None

class ZoneamentoVigenciaInput(BaseModel):
    data_inicio_vigencia: date

class ZoneamentoMotivoInput(BaseModel):
    motivo: str

class ZoneamentoParametrosInput(BaseModel):
    usos_permitidos: list[UsoPermitido] | None = None
    coeficiente_aproveitamento_max: Decimal | None = None
    taxa_ocupacao_max: Decimal | None = None
    gabarito_maximo: int | None = None
    recuo_frontal_minimo: Decimal | None = None
    permeabilidade_minima: Decimal | None = None
    area_lote_minima: Decimal | None = None

class ZoneamentoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_zoneamento: str
    nome: str
    tipo_zona: TipoZona
    status: StatusZoneamento
    plano_diretor_id: UUID
    provincia: str
    usos_permitidos: list[UsoPermitido]
    municipio: str | None = None
    coeficiente_aproveitamento_max: Decimal | None = None
    taxa_ocupacao_max: Decimal | None = None
    gabarito_maximo: int | None = None
    recuo_frontal_minimo: Decimal | None = None
    permeabilidade_minima: Decimal | None = None
    area_lote_minima: Decimal | None = None
    data_inicio_vigencia: date | None = None
    data_cadastro: date
    data_atualizacao: date | None = None
    observacoes: str | None = None