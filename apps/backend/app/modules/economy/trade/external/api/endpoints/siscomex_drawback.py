from apps.backend.app.modules.economy.trade.external.api.deps import get_siscomex_drawback_service
from apps.backend.app.modules.economy.trade.external.api.endpoints._habilitacao_router import (
    build_habilitacao_router,
)
from apps.backend.app.modules.economy.trade.external.api.schemas.siscomex_drawback_schema import (
    SiscomexDrawbackAprovacaoInput,
    SiscomexDrawbackCreate,
    SiscomexDrawbackRejeicaoInput,
    SiscomexDrawbackResponse,
)
from apps.backend.app.modules.economy.trade.external.exceptions import (
    InvalidSiscomexDrawbackStateError,
    SiscomexDrawbackAlreadyExistsError,
    SiscomexDrawbackNotFoundError,
)

router = build_habilitacao_router(
    prefix="/siscomex_drawback",
    tag="Comercio Externo - Siscomex Drawback",
    get_service=get_siscomex_drawback_service,
    create_schema=SiscomexDrawbackCreate,
    aprovacao_schema=SiscomexDrawbackAprovacaoInput,
    rejeicao_schema=SiscomexDrawbackRejeicaoInput,
    response_schema=SiscomexDrawbackResponse,
    already_exists_error_cls=SiscomexDrawbackAlreadyExistsError,
    not_found_error_cls=SiscomexDrawbackNotFoundError,
    invalid_state_error_cls=InvalidSiscomexDrawbackStateError,
)
