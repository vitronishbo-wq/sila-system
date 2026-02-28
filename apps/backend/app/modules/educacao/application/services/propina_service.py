from app.core.bridges import CitizenRepositoryPort, ServiceRequestLifecycleBridge
from app.modules.educacao.application.ports import PropinaRepositoryPort
from app.modules.educacao.application.services.workflow_service import WorkflowService


class PropinaService(WorkflowService):
    def __init__(self, repository: PropinaRepositoryPort, citizen_repo: CitizenRepositoryPort | None = None, request_service: ServiceRequestLifecycleBridge | None = None):
        super().__init__(repository=repository, process_prefix="PRP", citizen_repo=citizen_repo, request_service=request_service)
