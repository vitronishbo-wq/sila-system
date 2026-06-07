from __future__ import annotations

from dataclasses import dataclass

from apps.backend.app.modules.economy.trade.services.domain.enums import RamoComercial


@dataclass(frozen=True)
class RamoComercio:
    codigo: RamoComercial
    descricao: str
