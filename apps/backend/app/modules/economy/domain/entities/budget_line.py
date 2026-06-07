from dataclasses import dataclass


@dataclass
class BudgetLine:
    id: str
    ministry: str
    program: str
    allocated_amount: float
    spent_amount: float = 0.0

    def commit(self, amount: float) -> None:
        if self.spent_amount + amount > self.allocated_amount:
            raise ValueError("Budget exceeded")
        self.spent_amount += amount
