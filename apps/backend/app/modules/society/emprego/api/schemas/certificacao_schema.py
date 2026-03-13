from app.modules.society.emprego.api.schemas.workflow_schema import WorkflowAction, WorkflowCancel, WorkflowCreate, WorkflowResponse

class CertificacaoCreate(WorkflowCreate):
    pass

class CertificacaoAction(WorkflowAction):
    pass

class CertificacaoCancel(WorkflowCancel):
    pass

class CertificacaoResponse(WorkflowResponse):
    pass