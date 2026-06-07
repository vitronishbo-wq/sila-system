class TreasuryLedgerEngine:
    def record_revenue(self, ledger_repo, db, citizen_id: str, tax_id: str, amount: float):
        return ledger_repo.create(
            db,
            {
                "citizen_id": citizen_id,
                "tax_id": tax_id,
                "debit": 0.0,
                "credit": amount,
                "reference": "tax_payment",
            },
        )

    def record_expense(self, ledger_repo, db, reference: str, amount: float):
        return ledger_repo.create(
            db,
            {
                "citizen_id": None,
                "tax_id": None,
                "debit": amount,
                "credit": 0.0,
                "reference": reference,
            },
        )
