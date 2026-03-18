class ZeroTrustGateway:

    def __init__(self, identity_service, policy_engine):
        self.identity_service = identity_service
        self.policy_engine = policy_engine

    def authorize(self, source_service, target_service):
        identity = self.identity_service.get_identity(source_service)
        if not identity:
            raise Exception('unknown service')
        allowed = self.policy_engine.evaluate(source_service, target_service)
        if not allowed:
            raise Exception('zero trust policy denied')
        return True