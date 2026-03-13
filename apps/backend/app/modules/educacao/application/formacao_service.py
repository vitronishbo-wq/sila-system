from app.core.bridges import CitizenRepositoryPort, ServiceRequestLifecycleBridge
from app.modules.educacao.application.ports import FormacaoRepositoryPort
from app.modules.educacao.application.workflow_service import WorkflowService

class FormacaoService(WorkflowService):

    def __init__(self, repository: FormacaoRepositoryPort, citizen_repo: CitizenRepositoryPort | None=None, request_service: ServiceRequestLifecycleBridge | None=None):
        super().__init__(repository=repository, process_prefix='FRM', citizen_repo=citizen_repo, request_service=request_service)
