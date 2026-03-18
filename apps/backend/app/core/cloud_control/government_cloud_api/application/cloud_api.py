class GovernmentCloudAPI:

    def __init__(self, orchestrator, scheduler):
        self.orchestrator = orchestrator
        self.scheduler = scheduler

    def deploy_service(self, service_name, image):
        container = self.orchestrator.deploy_container(service_name, image)
        workload = {'container': container}
        node = self.scheduler.schedule(workload)
        return {'deployment': container, 'node': node}