class NationalPolicyEngine:

    def simulate_policy(

        self,
        policy_name,
        parameters

    ):

        simulation = {

            "policy": policy_name,
            "parameters": parameters,
            "impact": {

                "economic_growth": "+1.3%",
                "employment": "+0.8%",
                "public_spending": "+2.1%"

            }

        }

        return simulation
