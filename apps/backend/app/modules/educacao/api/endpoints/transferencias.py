from app.modules.educacao.api.deps import get_transferencia_service
from app.modules.educacao.api.endpoints._workflow_endpoints import build_workflow_router
from app.modules.educacao.api.schemas.transferencia_schema import TransferenciaCancelar, TransferenciaConcluir, TransferenciaCreate, TransferenciaResponse

router = build_workflow_router(
    tag="Educacao - Transferencias",
    get_service=get_transferencia_service,
    create_schema=TransferenciaCreate,
    response_schema=TransferenciaResponse,
    concluir_schema=TransferenciaConcluir,
    cancelar_schema=TransferenciaCancelar,
    routes=[
        ("/transferencias", "transferencia"),
        ("/transferencias/universitaria", "transferencia_universitaria"),
    ],
)
