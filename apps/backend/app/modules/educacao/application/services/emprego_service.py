from app.core.bridges import CitizenRepositoryPort, ServiceRequestLifecycleBridge
from app.modules.educacao.application.ports import EmpregoRepositoryPort
from app.modules.educacao.application.services.workflow_service import WorkflowService


class EmpregoService(WorkflowService):
    def __init__(self, repository: EmpregoRepositoryPort, citizen_repo: CitizenRepositoryPort | None = None, request_service: ServiceRequestLifecycleBridge | None = None):
        super().__init__(repository=repository, process_prefix="EMP", citizen_repo=citizen_repo, request_service=request_service)
