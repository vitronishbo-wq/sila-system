from apps.backend.app.modules.economy.trade.external.api.deps import (
    get_transportador_internacional_service,
)
from apps.backend.app.modules.economy.trade.external.api.endpoints._operador_logistico_router import (
    build_operador_logistico_router,
)
from apps.backend.app.modules.economy.trade.external.api.schemas.transportador_internacional_schema import (
    CancelamentoTransportadorInternacionalInput,
    HabilitacaoTransportadorInternacionalInput,
    SuspensaoTransportadorInternacionalInput,
    TransportadorInternacionalCreate,
    TransportadorInternacionalResponse,
)
from apps.backend.app.modules.economy.trade.external.exceptions import (
    InvalidTransportadorInternacionalStateError,
    TransportadorInternacionalAlreadyExistsError,
    TransportadorInternacionalNotFoundError,
)

router = build_operador_logistico_router(
    prefix="/transportadores-internacionais",
    tag="Comercio Externo - Transportadores Internacionais",
    get_service=get_transportador_internacional_service,
    create_schema=TransportadorInternacionalCreate,
    habilitacao_schema=HabilitacaoTransportadorInternacionalInput,
    suspensao_schema=SuspensaoTransportadorInternacionalInput,
    cancelamento_schema=CancelamentoTransportadorInternacionalInput,
    response_schema=TransportadorInternacionalResponse,
    already_exists_error_cls=TransportadorInternacionalAlreadyExistsError,
    not_found_error_cls=TransportadorInternacionalNotFoundError,
    invalid_state_error_cls=InvalidTransportadorInternacionalStateError,
)
