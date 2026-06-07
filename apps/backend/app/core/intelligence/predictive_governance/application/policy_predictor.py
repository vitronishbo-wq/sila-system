import numpy as np


class PolicyPredictor:
    """Predictive governance using trend analysis"""

    def forecast(self, data):
        """Forecast trend using polynomial regression"""
        if len(data) < 2:
            return "insufficient_data"
        trend = np.polyfit(range(len(data)), data, 1)
        slope = trend[0]
        if slope > 0:
            return "growth"
        if slope < 0:
            return "decline"
        return "stable"
