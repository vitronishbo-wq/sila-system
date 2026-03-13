from app.modules.society.emprego.api.schemas.workflow_schema import WorkflowAction, WorkflowCancel, WorkflowCreate, WorkflowResponse

class OfertaCreate(WorkflowCreate):
    pass

class OfertaAction(WorkflowAction):
    pass

class OfertaCancel(WorkflowCancel):
    pass

class OfertaResponse(WorkflowResponse):
    pass