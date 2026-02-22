class SilaMetrics:
    """Placeholder for metrics collection."""

    def __getattr__(self, name):
        # Return a dummy callable for any method call
        def dummy_method(*args, **kwargs):
            print(f"[METRICS] {name} called with {args} and {kwargs}")
            return self  # Allow chaining

        return dummy_method


sila_metrics = SilaMetrics()
