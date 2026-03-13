class RuntimePolicyEngine:

    def __init__(self):

        self.policies = {}

    def allow(

        self,
        source_service,
        target_service,

    ):

        if source_service not in self.policies:
            self.policies[source_service] = []

        self.policies[source_service].append(target_service)

    def evaluate(

        self,
        source_service,
        target_service,

    ):

        allowed = self.policies.get(source_service, [])

        return target_service in allowed
