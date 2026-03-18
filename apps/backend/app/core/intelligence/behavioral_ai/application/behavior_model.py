import numpy as np

class BehavioralModel:
    """Behavioral AI for user/system anomaly detection"""

    def detect_behavior_shift(self, history):
        """Detect significant changes in behavioral patterns"""
        if len(history) < 10:
            return False
        mean = np.mean(history[:-1])
        last = history[-1]
        deviation = abs(last - mean) / mean if mean != 0 else 0
        if deviation > 0.5:
            return True
        return False