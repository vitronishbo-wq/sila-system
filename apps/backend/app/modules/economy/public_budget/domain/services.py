from datetime import date
from decimal import Decimal
from uuid import uuid4
from .entities import BudgetCommitment, BudgetLiquidation, BudgetPayment, PublicProgram

class BudgetExecutionService:

    def commit_budget(self, program: PublicProgram, amount: Decimal) -> BudgetCommitment:
        if program.spent + amount > program.allocated_budget:
            raise ValueError('Orcamento insuficiente')
        return BudgetCommitment(id=uuid4(), program_id=program.id, amount=amount, created_at=date.today())

    def liquidate_commitment(self, commitment: BudgetCommitment) -> BudgetLiquidation:
        return BudgetLiquidation(id=uuid4(), commitment_id=commitment.id, amount=commitment.amount, created_at=date.today())

    def authorize_payment(self, liquidation: BudgetLiquidation) -> BudgetPayment:
        return BudgetPayment(id=uuid4(), liquidation_id=liquidation.id, amount=liquidation.amount, created_at=date.today())