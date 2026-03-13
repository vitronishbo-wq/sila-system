from dataclasses import dataclass

@dataclass
class TreasuryAccount:
    id: str
    code: str
    name: str
    balance: float = 0.0

    def credit(self, amount: float) -> None:
        self.balance += amount

    def debit(self, amount: float) -> None:
        if amount > self.balance:
            raise ValueError('Insufficient treasury balance')
        self.balance -= amount