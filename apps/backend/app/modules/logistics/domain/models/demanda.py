from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal

@dataclass
class DemandaOperacional:
    viagens_total: int
    passageiros_total: int
    passageiros_media_por_viagem: Decimal
    arrecadacao_total: Decimal