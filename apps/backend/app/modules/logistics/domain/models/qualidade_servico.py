from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass
class QualidadeServico:
    viagens_total: int
    viagens_concluidas: int
    viagens_canceladas: int
    viagens_atrasadas: int
    pontualidade_percentual: Decimal
    taxa_cancelamento_percentual: Decimal
    taxa_atraso_percentual: Decimal
