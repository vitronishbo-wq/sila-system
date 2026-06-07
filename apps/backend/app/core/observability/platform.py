class NationalObservabilityPlatform:
    def __init__(self, tracer, metrics, logger, anomaly_detector):
        self.tracer = tracer
        self.metrics = metrics
        self.logger = logger
        self.anomaly_detector = anomaly_detector

    def record_request(self, service, operation):
        trace = self.tracer.start_trace(service)
        self.tracer.add_span(trace, operation)
        self.metrics.increment("requests_total")
        self.logger.log(service, "INFO", f"operation {operation}")
        return trace
