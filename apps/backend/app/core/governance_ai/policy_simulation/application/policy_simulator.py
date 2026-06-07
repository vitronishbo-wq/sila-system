class PolicySimulator:
    def __init__(self):
        self.policies = {}

    def register_policy(self, name, parameters):
        self.policies[name] = parameters

    def simulate(self, policy_name, dataset):
        policy = self.policies.get(policy_name)
        if not policy:
            raise Exception("policy not registered")
        impact = len(dataset) * policy.get("impact_factor", 1)
        return {"policy": policy_name, "estimated_impact": impact}
