from __future__ import annotations

from importlib import import_module

from sqlalchemy.orm import Session

from apps.backend.app.platform.persistence.unit_of_work import UnitOfWork

from ....infrastructure.repositories.tax_ledger_repository import TaxLedgerRepository
from ...domain.services.treasury_ledger_engine import TreasuryLedgerEngine
from ...infrastructure.repositories.treasury_account_repository import TreasuryAccountRepository


class _FallbackPaymentService:
    def create_payment(self, db, data: dict):
        return {
            "id": None,
            "citizen_id": data.get("citizen_id"),
            "amount": data.get("amount"),
            "type": data.get("type"),
            "status": "created",
        }


def _resolve_payment_service():
    try:
        module = import_module("apps.backend.app.modules.payment.services.payment_service")
        service_cls = getattr(module, "PaymentService", None)
        if service_cls is None:
            return _FallbackPaymentService()
        return service_cls()
    except Exception:
        return _FallbackPaymentService()


class TreasuryService:
    def __init__(self):
        self.ledger_repo = TaxLedgerRepository()
        self.payment = _resolve_payment_service()
        self.account_repo = TreasuryAccountRepository()
        self.engine = TreasuryLedgerEngine()

    def receive_tax_payment(self, db: Session, citizen_id: str, tax_id: str, amount: float):
        with UnitOfWork(db):
            payment = self.payment.create_payment(
                db, {"citizen_id": citizen_id, "amount": amount, "type": "tax"}
            )
            ledger = self.engine.record_revenue(self.ledger_repo, db, citizen_id, tax_id, amount)
            treasury = self.account_repo.get_by_id(db, "TREASURY_MAIN")
            if treasury:
                treasury.balance += amount
                db.flush()
            return {"payment": payment, "ledger": ledger}

    def execute_expense(self, db: Session, reference: str, amount: float):
        with UnitOfWork(db):
            treasury = self.account_repo.get_by_id(db, "TREASURY_MAIN")
            if treasury is None:
                raise ValueError("Treasury account not found")
            if treasury.balance < amount:
                raise ValueError("Treasury insufficient funds")
            treasury.balance -= amount
            ledger = self.engine.record_expense(self.ledger_repo, db, reference, amount)
            db.flush()
            return ledger
