class DataSources:
    """Connector façade for BI to read metrics from other modules.

    Implementors should provide methods to fetch metrics from each system.
    """

    def __init__(self, clients: dict):
        self.clients = clients

    def service_requests_metrics(self, **kwargs):
        return []

    def workflow_metrics(self, **kwargs):
        return []

    def finance_metrics(self, **kwargs):
        return []

    def citizen_metrics(self, **kwargs):
        return []
