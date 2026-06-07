from __future__ import annotations

from dataclasses import dataclass

from apps.backend.app.modules.industry.domain.enums import RamoIndustrial


@dataclass(frozen=True)
class Ramo:
    codigo: RamoIndustrial
    descricao: str
