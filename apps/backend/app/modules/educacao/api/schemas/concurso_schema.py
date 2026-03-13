from apps.backend.app.modules.educacao.api.schemas.workflow_schema import WorkflowCancelar, WorkflowConcluir, WorkflowCreate, WorkflowResponse

class ConcursoCreate(WorkflowCreate):
    pass

class ConcursoResponse(WorkflowResponse):
    pass

class ConcursoConcluir(WorkflowConcluir):
    pass

class ConcursoCancelar(WorkflowCancelar):
    pass