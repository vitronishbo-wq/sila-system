class GovernmentServicePortal:

    def __init__(self):

        self.services = {}

    def register_service(

        self,
        name,
        endpoint

    ):

        self.services[name] = endpoint

    def list_services(self):

        return self.services
