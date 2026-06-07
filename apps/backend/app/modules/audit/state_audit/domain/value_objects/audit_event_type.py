from enum import StrEnum


class AuditEventType(StrEnum):
    TAX_COLLECTED = "TaxCollected"
    BUDGET_COMMITTED = "BudgetCommitted"
    TENDER_CREATED = "TenderCreated"
    CONTRACT_AWARDED = "ContractAwarded"
    PAYMENT_EXECUTED = "PaymentExecuted"
