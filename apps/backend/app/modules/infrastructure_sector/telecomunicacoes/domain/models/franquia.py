from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Franquia:
    franquia_gb: Decimal
    preco_excedente_gb: Decimal

    @classmethod
    def padrao(cls) -> Franquia:
        return cls(franquia_gb=Decimal("100.00"), preco_excedente_gb=Decimal("2.50"))

    def calcular_excedente(self, total_gb: Decimal) -> Decimal:
        if total_gb <= self.franquia_gb:
            return Decimal("0.00")
        return (total_gb - self.franquia_gb).quantize(Decimal("0.01"))

    def calcular_valor_excedente(self, total_gb: Decimal) -> Decimal:
        excedente = self.calcular_excedente(total_gb)
        return (excedente * self.preco_excedente_gb).quantize(Decimal("0.01"))
