from apps.backend.app.modules.educacao.api.schemas.workflow_schema import (
    WorkflowCancelar,
    WorkflowConcluir,
    WorkflowCreate,
    WorkflowResponse,
)


class EmpregoCreate(WorkflowCreate):
    pass


class EmpregoResponse(WorkflowResponse):
    pass


class EmpregoConcluir(WorkflowConcluir):
    pass


class EmpregoCancelar(WorkflowCancelar):
    pass
