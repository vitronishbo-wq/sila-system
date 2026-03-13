from uuid import uuid4
from app.modules.procurement.domain.entities.bid import Bid
from app.modules.procurement.domain.services.procurement_engine import ProcurementEngine

def test_evaluate_lowest_price():
    b1 = Bid(tender_id=uuid4(), supplier_id=uuid4(), amount=100.0)
    b2 = Bid(tender_id=uuid4(), supplier_id=uuid4(), amount=80.0)
    winner = ProcurementEngine.evaluate_lowest_price([b1, b2])
    assert winner.amount == 80.0
