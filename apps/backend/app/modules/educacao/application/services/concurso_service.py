from app.core.bridges import CitizenRepositoryPort, ServiceRequestLifecycleBridge
from app.modules.educacao.application.ports import ConcursoRepositoryPort
from app.modules.educacao.application.services.workflow_service import WorkflowService


class ConcursoService(WorkflowService):
    def __init__(self, repository: ConcursoRepositoryPort, citizen_repo: CitizenRepositoryPort | None = None, request_service: ServiceRequestLifecycleBridge | None = None):
        super().__init__(repository=repository, process_prefix="CNC", citizen_repo=citizen_repo, request_service=request_service)
