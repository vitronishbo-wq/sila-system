class FraudEngine:
    """Fraud detection for financial and governmental operations"""

    rules = {"tax": 10000000, "transfer": 5000000, "payment": 1000000}

    def detect(self, operation, value):
        """Detect fraud based on operation thresholds"""
        limit = self.rules.get(operation)
        if not limit:
            return False
        if value > limit:
            return True
        return False
