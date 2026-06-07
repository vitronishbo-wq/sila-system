from apps.backend.app.modules.economy.trade.external.api.deps import (
    get_drawback_interno_service_protected,
)
from apps.backend.app.modules.economy.trade.external.api.endpoints._habilitacao_router import (
    build_habilitacao_router,
)
from apps.backend.app.modules.economy.trade.external.api.schemas.drawback_interno_schema import (
    DrawbackInternoAprovacaoInput,
    DrawbackInternoCreate,
    DrawbackInternoRejeicaoInput,
    DrawbackInternoResponse,
)
from apps.backend.app.modules.economy.trade.external.exceptions import (
    DrawbackInternoAlreadyExistsError,
    DrawbackInternoNotFoundError,
    InvalidDrawbackInternoStateError,
)

router = build_habilitacao_router(
    prefix="/drawback_interno",
    tag="Comercio Externo - Drawback Interno",
    get_service=get_drawback_interno_service_protected,
    create_schema=DrawbackInternoCreate,
    aprovacao_schema=DrawbackInternoAprovacaoInput,
    rejeicao_schema=DrawbackInternoRejeicaoInput,
    response_schema=DrawbackInternoResponse,
    already_exists_error_cls=DrawbackInternoAlreadyExistsError,
    not_found_error_cls=DrawbackInternoNotFoundError,
    invalid_state_error_cls=InvalidDrawbackInternoStateError,
)
