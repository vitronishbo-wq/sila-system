from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID


@dataclass
class Budget:
    id: UUID
    fiscal_year: int
    approved: bool
    total_revenue: Decimal
    total_expense: Decimal


@dataclass
class MinistryBudget:
    id: UUID
    ministry_id: UUID
    budget_id: UUID
    allocated_amount: Decimal


@dataclass
class PublicProgram:
    id: UUID
    name: str
    ministry_id: UUID
    allocated_budget: Decimal
    spent: Decimal = Decimal("0.00")


@dataclass
class BudgetCommitment:
    id: UUID
    program_id: UUID
    amount: Decimal
    created_at: date


@dataclass
class BudgetLiquidation:
    id: UUID
    commitment_id: UUID
    amount: Decimal
    created_at: date


@dataclass
class BudgetPayment:
    id: UUID
    liquidation_id: UUID
    amount: Decimal
    created_at: date
