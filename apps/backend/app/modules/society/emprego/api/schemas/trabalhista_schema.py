from app.modules.society.emprego.api.schemas.workflow_schema import WorkflowAction, WorkflowCancel, WorkflowCreate, WorkflowResponse

class TrabalhistaCreate(WorkflowCreate):
    pass

class TrabalhistaAction(WorkflowAction):
    pass

class TrabalhistaCancel(WorkflowCancel):
    pass

class TrabalhistaResponse(WorkflowResponse):
    pass