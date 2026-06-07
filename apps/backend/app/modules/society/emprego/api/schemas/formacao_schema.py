from apps.backend.app.modules.society.emprego.api.schemas.workflow_schema import (
    WorkflowAction,
    WorkflowCancel,
    WorkflowCreate,
    WorkflowResponse,
)


class FormacaoCreate(WorkflowCreate):
    pass


class FormacaoAction(WorkflowAction):
    pass


class FormacaoCancel(WorkflowCancel):
    pass


class FormacaoResponse(WorkflowResponse):
    pass
