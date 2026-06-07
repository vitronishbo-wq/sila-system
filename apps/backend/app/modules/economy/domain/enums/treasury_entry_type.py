from enum import StrEnum


class TreasuryEntryType(StrEnum):
    REVENUE = "revenue"
    EXPENSE = "expense"
    TRANSFER = "transfer"
