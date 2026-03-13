from app.modules.educacao.api.schemas.workflow_schema import WorkflowCancelar, WorkflowConcluir, WorkflowCreate, WorkflowResponse

class CertificadoCreate(WorkflowCreate):
    pass

class CertificadoResponse(WorkflowResponse):
    pass

class CertificadoConcluir(WorkflowConcluir):
    pass

class CertificadoCancelar(WorkflowCancelar):
    pass