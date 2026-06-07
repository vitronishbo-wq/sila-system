class EconomicForecaster:
    def forecast_growth(self, gdp, investment, inflation):
        growth = investment * 0.3 - inflation * 0.2 + gdp * 0.1
        return {"predicted_growth": growth}
