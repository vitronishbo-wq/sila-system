from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

@dataclass
class CreateBudget:
    fiscal_year: int
    total_revenue: Decimal
    total_expense: Decimal

@dataclass
class CreateProgram:
    name: str
    ministry_id: UUID
    allocated_budget: Decimal

@dataclass
class CommitBudget:
    program_id: UUID
    amount: Decimal

@dataclass
class LiquidateCommitment:
    commitment_id: UUID

@dataclass
class PayLiquidation:
    liquidation_id: UUID