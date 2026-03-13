class PolicyEngine:

    def __init__(self):

        self.policies = {}

    def register_policy(

        self,
        service,
        required_roles

    ):

        self.policies[service] = required_roles

    def authorize(

        self,
        service,
        user_roles

    ):

        required = self.policies.get(service)

        if not required:
            return True

        for role in user_roles:
            if role in required:
                return True

        return False
