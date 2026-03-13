class EconomicEngine:

    def __init__(self):
        self.markets = []

    def register_market(self, market):
        self.markets.append(market)

    def apply_policy(self, policy):
        for market in self.markets:
            policy.apply(market)