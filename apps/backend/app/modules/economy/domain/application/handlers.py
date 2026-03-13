from __future__ import annotations
from apps.backend.app.platform.persistence.unit_of_work import UnitOfWork
from apps.backend.app.modules.economy.application.services.treasury_service import TreasuryService
from ..domain.services import BudgetExecutionService

class CommitBudgetHandler:

    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.execution = BudgetExecutionService()

    def handle(self, cmd, program):
        with self.uow:
            commitment = self.execution.commit_budget(program, cmd.amount)
            return commitment

class PayLiquidationHandler:

    def __init__(self, uow: UnitOfWork, treasury: TreasuryService):
        self.uow = uow
        self.treasury = treasury
        self.execution = BudgetExecutionService()

    def handle(self, cmd, liquidation, db):
        with self.uow:
            payment = self.execution.authorize_payment(liquidation)
            self.treasury.execute_expense(db, 'budget_execution', float(payment.amount))
            return payment
