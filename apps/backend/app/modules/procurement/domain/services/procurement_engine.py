from ..entities.bid import Bid


class ProcurementEngine:
    @staticmethod
    def evaluate_lowest_price(bids: list[Bid]) -> Bid:
        if not bids:
            raise ValueError("No bids submitted")
        return min(bids, key=lambda b: b.amount)
