from __future__ import annotations
from dataclasses import dataclass
from app.modules.economy.trade.services.domain.enums import PorteComercial

@dataclass(frozen=True)
class PorteComercio:
    codigo: PorteComercial
    descricao: str