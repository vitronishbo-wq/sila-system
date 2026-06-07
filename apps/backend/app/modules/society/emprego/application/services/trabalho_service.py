from apps.backend.app.modules.society.emprego.application.ports import (
    CitizenServicePort,
    RequestServicePort,
    WorkflowRepositoryPort,
)
from apps.backend.app.modules.society.emprego.application.services.workflow_service import (
    WorkflowService,
)


class TrabalhoService(WorkflowService):
    def __init__(
        self,
        *,
        repository: WorkflowRepositoryPort,
        citizen_service: CitizenServicePort | None = None,
        request_service: RequestServicePort | None = None,
    ):
        super().__init__(
            repository=repository,
            process_prefix="TRAB",
            citizen_service=citizen_service,
            request_service=request_service,
        )
