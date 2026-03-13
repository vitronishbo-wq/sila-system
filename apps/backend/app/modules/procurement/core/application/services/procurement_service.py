from uuid import UUID
from ...domain.entities.contract import Contract
from ...domain.services.procurement_engine import ProcurementEngine

class ProcurementService:

    def __init__(self, tender_repo, contract_repo, treasury_service=None, budget_service=None):
        self.tender_repo = tender_repo
        self.contract_repo = contract_repo
        self.treasury = treasury_service
        self.budget = budget_service

    def evaluate_tender(self, tender_id: UUID):
        tender = self.tender_repo.get(tender_id)
        winner = ProcurementEngine.evaluate_lowest_price(tender.bids)
        contract = Contract(tender_id=tender.id, supplier_id=winner.supplier_id, value=winner.amount)
        self.contract_repo.save(contract)
        return contract