from decimal import Decimal


class BudgetPolicy:
    @staticmethod
    def ensure_non_negative(amount: Decimal) -> None:
        if amount < Decimal("0"):
            raise ValueError("Amount must be non-negative")
