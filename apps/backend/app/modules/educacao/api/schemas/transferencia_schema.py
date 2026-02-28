from app.modules.educacao.api.schemas.workflow_schema import (
    WorkflowCancelar,
    WorkflowConcluir,
    WorkflowCreate,
    WorkflowResponse,
)


class TransferenciaCreate(WorkflowCreate):
    pass


class TransferenciaResponse(WorkflowResponse):
    pass


class TransferenciaConcluir(WorkflowConcluir):
    pass


class TransferenciaCancelar(WorkflowCancelar):
    pass
