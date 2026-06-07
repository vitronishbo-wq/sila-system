class AnomalyDetector:
    def __init__(self):
        self.thresholds = {}

    def register_threshold(self, metric, limit):
        self.thresholds[metric] = limit

    def evaluate(self, metric, value):
        limit = self.thresholds.get(metric)
        if limit is None:
            return False
        return value > limit
