import uuid


class NationalContainerOrchestrator:

    def __init__(self):

        self.containers = {}

    def deploy_container(

        self,
        service_name,
        image

    ):

        container_id = str(uuid.uuid4())

        self.containers[container_id] = {

            "service": service_name,
            "image": image,
            "status": "running"

        }

        return self.containers[container_id]

    def list_containers(self):

        return self.containers
