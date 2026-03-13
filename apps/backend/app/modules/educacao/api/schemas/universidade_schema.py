from app.modules.educacao.api.schemas.workflow_schema import WorkflowCancelar, WorkflowConcluir, WorkflowCreate, WorkflowResponse

class UniversidadeCreate(WorkflowCreate):
    pass

class UniversidadeResponse(WorkflowResponse):
    pass

class UniversidadeConcluir(WorkflowConcluir):
    pass

class UniversidadeCancelar(WorkflowCancelar):
    pass