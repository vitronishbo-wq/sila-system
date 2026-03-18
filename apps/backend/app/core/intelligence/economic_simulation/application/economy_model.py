import random

class EconomyModel:
    """Economic simulation engine for policy analysis"""

    def simulate(self, gdp, inflation):
        """Simulate economic outcomes"""
        growth_factor = random.uniform(0.9, 1.1)
        new_gdp = gdp * growth_factor
        inflation_adjusted = inflation * random.uniform(0.95, 1.05)
        return {'gdp': new_gdp, 'inflation': inflation_adjusted}