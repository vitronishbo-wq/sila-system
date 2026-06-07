class SovereignMetricsRegistry:
    def __init__(self):
        self.metrics = {}

    def increment(self, metric_name, value=1):
        if metric_name not in self.metrics:
            self.metrics[metric_name] = 0
        self.metrics[metric_name] += value

    def set_metric(self, metric_name, value):
        self.metrics[metric_name] = value

    def get_metric(self, metric_name):
        return self.metrics.get(metric_name)
