from app.modules.society.emprego.api.schemas.workflow_schema import WorkflowAction, WorkflowCancel, WorkflowCreate, WorkflowResponse

class MediacaoCreate(WorkflowCreate):
    pass

class MediacaoAction(WorkflowAction):
    pass

class MediacaoCancel(WorkflowCancel):
    pass

class MediacaoResponse(WorkflowResponse):
    pass