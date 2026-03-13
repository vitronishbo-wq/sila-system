from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP

@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str = 'AOA'

    def __post_init__(self) -> None:
        if self.amount < Decimal('0'):
            raise ValueError('Money amount cannot be negative')

    def quantized(self) -> Decimal:
        return self.amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)