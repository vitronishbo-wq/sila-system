import random


class EconomyModel:
    """Economic simulation engine for policy analysis"""

    def simulate(self, gdp, inflation):
        """Simulate economic outcomes"""
        # Apply random growth factor between 0.9x and 1.1x
        growth_factor = random.uniform(0.9, 1.1)
        new_gdp = gdp * growth_factor

        # Adjust inflation with variance
        inflation_adjusted = inflation * random.uniform(0.95, 1.05)

        return {
            "gdp": new_gdp,
            "inflation": inflation_adjusted
        }
