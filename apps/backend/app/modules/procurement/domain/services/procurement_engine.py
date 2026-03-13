from typing import List
from ..entities.bid import Bid

class ProcurementEngine:

    @staticmethod
    def evaluate_lowest_price(bids: List[Bid]) -> Bid:
        if not bids:
            raise ValueError('No bids submitted')
        return min(bids, key=lambda b: b.amount)