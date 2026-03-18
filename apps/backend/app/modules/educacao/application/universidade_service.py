from apps.backend.app.core.bridges import CitizenRepositoryPort, ServiceRequestLifecycleBridge
from apps.backend.app.modules.educacao.application.ports import UniversidadeRepositoryPort
from apps.backend.app.modules.educacao.application.workflow_service import WorkflowService

class UniversidadeService(WorkflowService):

    def __init__(self, repository: UniversidadeRepositoryPort, citizen_repo: CitizenRepositoryPort | None=None, request_service: ServiceRequestLifecycleBridge | None=None):
        super().__init__(repository=repository, process_prefix='UNI', citizen_repo=citizen_repo, request_service=request_service)