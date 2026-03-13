import uuid


class ServiceIdentityManager:

    def __init__(self):

        self.services = {}

    def register_service(

        self,
        name,
        secret

    ):

        service_id = str(uuid.uuid4())

        self.services[name] = {

            "id": service_id,
            "secret": secret

        }

        return service_id

    def authenticate(

        self,
        name,
        secret

    ):

        service = self.services.get(name)

        if not service:
            return False

        return service["secret"] == secret
