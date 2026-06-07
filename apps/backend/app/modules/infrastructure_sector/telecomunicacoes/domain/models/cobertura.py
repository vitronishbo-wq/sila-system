from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Cobertura:
    municipio: str
    provincia: str
    tecnologia: str
    percentual_cobertura: Decimal

    @classmethod
    def registrar(
        cls, *, municipio: str, provincia: str, tecnologia: str, percentual_cobertura: Decimal
    ) -> Cobertura:
        if percentual_cobertura < Decimal("0") or percentual_cobertura > Decimal("100"):
            raise ValueError("Percentual de cobertura deve estar entre 0 e 100")
        return cls(
            municipio=municipio.strip(),
            provincia=provincia.strip(),
            tecnologia=tecnologia.strip().upper(),
            percentual_cobertura=percentual_cobertura.quantize(Decimal("0.01")),
        )
