class CrisisEngine:
    """Crisis risk prediction and evaluation"""

    def evaluate(self, indicators):
        """Evaluate crisis risk based on indicators"""
        score = 0
        for indicator, value in indicators.items():
            if value > 0.8:
                score += 1
        if score >= 3:
            return 'high_risk'
        if score == 2:
            return 'medium_risk'
        return 'low_risk'