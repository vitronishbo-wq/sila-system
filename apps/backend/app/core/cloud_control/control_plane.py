class SovereignCloudControlPlane:

    def __init__(self, compute_grid, orchestrator, scheduler, api):
        self.compute_grid = compute_grid
        self.orchestrator = orchestrator
        self.scheduler = scheduler
        self.api = api

    def deploy(self, service, image):
        return self.api.deploy_service(service, image)