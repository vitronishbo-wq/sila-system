class PolicyMetrics:

    def __init__(self):
        self.results = []

    def record(self, result):
        self.results.append(result)