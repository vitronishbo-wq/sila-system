from app.modules.society.emprego.api.schemas.workflow_schema import WorkflowAction, WorkflowCancel, WorkflowCreate, WorkflowResponse

class ConcursoCreate(WorkflowCreate):
    pass

class ConcursoAction(WorkflowAction):
    pass

class ConcursoCancel(WorkflowCancel):
    pass

class ConcursoResponse(WorkflowResponse):
    pass