from enum import Enum

class TreasuryEntryType(str, Enum):
    REVENUE = 'revenue'
    EXPENSE = 'expense'
    TRANSFER = 'transfer'