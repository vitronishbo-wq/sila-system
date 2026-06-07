from apps.backend.app.modules.educacao.api.schemas.workflow_schema import (
    WorkflowCancelar,
    WorkflowConcluir,
    WorkflowCreate,
    WorkflowResponse,
)


class BoletimCreate(WorkflowCreate):
    pass


class BoletimResponse(WorkflowResponse):
    pass


class BoletimConcluir(WorkflowConcluir):
    pass


class BoletimCancelar(WorkflowCancelar):
    pass
