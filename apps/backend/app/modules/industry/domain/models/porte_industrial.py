from __future__ import annotations
from dataclasses import dataclass
from apps.backend.app.modules.industry.domain.enums import PorteIndustrial

@dataclass(frozen=True)
class Porte:
    codigo: PorteIndustrial
    descricao: str
