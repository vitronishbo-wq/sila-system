from app.modules.educacao.api.schemas.workflow_schema import WorkflowCancelar, WorkflowConcluir, WorkflowCreate, WorkflowResponse

class PropinaCreate(WorkflowCreate):
    pass

class PropinaResponse(WorkflowResponse):
    pass

class PropinaConcluir(WorkflowConcluir):
    pass

class PropinaCancelar(WorkflowCancelar):
    pass