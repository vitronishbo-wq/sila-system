from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict

from apps.backend.app.modules.infrastructure_sector.aviacao_civil.domain.enums import TipoAeroporto


class AeroportoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_iata: str
    codigo_icao: str
    nome: str
    tipo: TipoAeroporto
    municipio_id: UUID
    coordenadas: dict[str, float]
    altitude_m: int
    fuso_horario: str
    administracao: str
