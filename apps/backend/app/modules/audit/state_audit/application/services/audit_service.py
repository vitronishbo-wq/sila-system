class AuditService:
    def __init__(self, audit_engine, log_repo, case_repo):
        self.engine = audit_engine
        self.logs = log_repo
        self.cases = case_repo

    def register_event(self, event):
        self.logs.save(event)
        alerts = self.engine.evaluate(event)
        for alert in alerts:
            self.cases.open_case(alert)
        return alerts
