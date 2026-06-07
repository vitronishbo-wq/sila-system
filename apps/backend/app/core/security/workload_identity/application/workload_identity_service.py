import hashlib
import uuid


class WorkloadIdentityService:
    def __init__(self):
        self.identities = {}

    def register_service(self, service_name: str):
        identity = str(uuid.uuid4())
        secret = hashlib.sha256(identity.encode()).hexdigest()
        self.identities[service_name] = {"identity": identity, "secret": secret}
        return self.identities[service_name]

    def get_identity(self, service_name):
        return self.identities.get(service_name)
