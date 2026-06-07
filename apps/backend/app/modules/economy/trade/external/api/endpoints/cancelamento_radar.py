from apps.backend.app.modules.economy.trade.external.api.deps import get_cancelamento_radar_service
from apps.backend.app.modules.economy.trade.external.api.endpoints._habilitacao_router import (
    build_habilitacao_router,
)
from apps.backend.app.modules.economy.trade.external.api.schemas.cancelamento_radar_schema import (
    CancelamentoRadarAprovacaoInput,
    CancelamentoRadarCreate,
    CancelamentoRadarRejeicaoInput,
    CancelamentoRadarResponse,
)
from apps.backend.app.modules.economy.trade.external.exceptions import (
    CancelamentoRadarAlreadyExistsError,
    CancelamentoRadarNotFoundError,
    InvalidCancelamentoRadarStateError,
)

router = build_habilitacao_router(
    prefix="/cancelamento_radar",
    tag="Comercio Externo - Cancelamento Radar",
    get_service=get_cancelamento_radar_service,
    create_schema=CancelamentoRadarCreate,
    aprovacao_schema=CancelamentoRadarAprovacaoInput,
    rejeicao_schema=CancelamentoRadarRejeicaoInput,
    response_schema=CancelamentoRadarResponse,
    already_exists_error_cls=CancelamentoRadarAlreadyExistsError,
    not_found_error_cls=CancelamentoRadarNotFoundError,
    invalid_state_error_cls=InvalidCancelamentoRadarStateError,
)
