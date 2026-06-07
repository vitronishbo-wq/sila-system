from dataclasses import dataclass


@dataclass
class FiscalTransfer:
    id: str
    from_account: str
    to_account: str
    amount: float
    reference: str
