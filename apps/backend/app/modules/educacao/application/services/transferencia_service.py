from app.core.bridges import CitizenRepositoryPort, ServiceRequestLifecycleBridge
from app.modules.educacao.application.ports import TransferenciaRepositoryPort
from app.modules.educacao.application.services.workflow_service import WorkflowService


class TransferenciaService(WorkflowService):
    def __init__(self, repository: TransferenciaRepositoryPort, citizen_repo: CitizenRepositoryPort | None = None, request_service: ServiceRequestLifecycleBridge | None = None):
        super().__init__(repository=repository, process_prefix="TRF", citizen_repo=citizen_repo, request_service=request_service)
