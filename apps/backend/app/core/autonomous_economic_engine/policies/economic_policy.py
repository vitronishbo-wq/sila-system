class EconomicPolicy:

    def __init__(self, name):
        self.name = name

    def apply(self, market):
        market.supply *= 1.02