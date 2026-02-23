class DataSources:
    def __init__(self, clients: dict):
        self.clients = clients

    def workflow_metrics(self, **kwargs):
        return []

    def service_requests_metrics(self, **kwargs):
        return []

    def finances_metrics(self, **kwargs):
        return []

    def health_metrics(self, **kwargs):
        return []

    def civil_registry_metrics(self, **kwargs):
        return []
