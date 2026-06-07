from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.enums import (
    StatusEspectro,
    TipoEspectro,
    TipoServico,
)


class EspectroCreate(BaseModel):
    tipo: TipoEspectro
    frequencia_inicial_mhz: float = Field(..., ge=0)
    frequencia_final_mhz: float = Field(..., gt=0)
    servico_principal: TipoServico
    municipio: str
    provincia: str
    outorga_id: UUID | None = None
    observacoes: str | None = None


class EspectroStatusUpdate(BaseModel):
    status: StatusEspectro


class EspectroVincularOutorga(BaseModel):
    outorga_id: UUID


class EspectroResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_espectro: str
    tipo: TipoEspectro
    frequencia_inicial_mhz: float
    frequencia_final_mhz: float
    largura_banda_mhz: float
    servico_principal: TipoServico
    municipio: str
    provincia: str
    status: StatusEspectro
    outorga_id: UUID | None = None
    ativo: bool
