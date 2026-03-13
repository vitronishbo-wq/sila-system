from app.core.bridges import CitizenRepositoryPort, ServiceRequestLifecycleBridge
from apps.backend.app.modules.educacao.application.ports import BoletimRepositoryPort
from apps.backend.app.modules.educacao.application.workflow_service import WorkflowService


class BoletimService(WorkflowService):

    def __init__(
        self,
        repository: BoletimRepositoryPort,
        citizen_repo: CitizenRepositoryPort | None = None,
        request_service: ServiceRequestLifecycleBridge | None = None,
    ):
        super().__init__(
            repository=repository,
            process_prefix="BLT",
            citizen_repo=citizen_repo,
            request_service=request_service,
        )
