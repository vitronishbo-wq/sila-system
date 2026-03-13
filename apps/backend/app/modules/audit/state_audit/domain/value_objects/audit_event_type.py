from enum import Enum

class AuditEventType(str, Enum):
    TAX_COLLECTED = 'TaxCollected'
    BUDGET_COMMITTED = 'BudgetCommitted'
    TENDER_CREATED = 'TenderCreated'
    CONTRACT_AWARDED = 'ContractAwarded'
    PAYMENT_EXECUTED = 'PaymentExecuted'