from app.modules.educacao.api.schemas.workflow_schema import WorkflowCancelar, WorkflowConcluir, WorkflowCreate, WorkflowResponse

class FormacaoCreate(WorkflowCreate):
    pass

class FormacaoResponse(WorkflowResponse):
    pass

class FormacaoConcluir(WorkflowConcluir):
    pass

class FormacaoCancelar(WorkflowCancelar):
    pass