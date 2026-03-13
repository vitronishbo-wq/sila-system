class PolicyLinter:

    REQUIRED_POLICIES = [

        "audit_logging",
        "security_validation",
        "event_emission"

    ]

    def validate(self, service_config):

        missing = []

        for policy in self.REQUIRED_POLICIES:

            if policy not in service_config:

                missing.append(policy)

        return {

            "valid": len(missing) == 0,
            "missing": missing

        }
