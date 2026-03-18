import statistics

class AnomalyEngine:
    """Statistical anomaly detection using Z-score"""

    def detect(self, metrics):
        """Detect anomalies using standard deviation threshold"""
        if len(metrics) < 5:
            return False
        mean = statistics.mean(metrics)
        stdev = statistics.stdev(metrics)
        last = metrics[-1]
        z_score = (last - mean) / stdev if stdev else 0
        if abs(z_score) > 3:
            return True
        return False