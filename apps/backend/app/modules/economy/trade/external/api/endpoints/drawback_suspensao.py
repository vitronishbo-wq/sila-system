from apps.backend.app.modules.economy.trade.external.api.deps import (
    get_drawback_suspensao_service_protected,
)
from apps.backend.app.modules.economy.trade.external.api.endpoints._habilitacao_router import (
    build_habilitacao_router,
)
from apps.backend.app.modules.economy.trade.external.api.schemas.drawback_suspensao_schema import (
    DrawbackSuspensaoAprovacaoInput,
    DrawbackSuspensaoCreate,
    DrawbackSuspensaoRejeicaoInput,
    DrawbackSuspensaoResponse,
)
from apps.backend.app.modules.economy.trade.external.exceptions import (
    DrawbackSuspensaoAlreadyExistsError,
    DrawbackSuspensaoNotFoundError,
    InvalidDrawbackSuspensaoStateError,
)

router = build_habilitacao_router(
    prefix="/drawback_suspensao",
    tag="Comercio Externo - Drawback Suspensao",
    get_service=get_drawback_suspensao_service_protected,
    create_schema=DrawbackSuspensaoCreate,
    aprovacao_schema=DrawbackSuspensaoAprovacaoInput,
    rejeicao_schema=DrawbackSuspensaoRejeicaoInput,
    response_schema=DrawbackSuspensaoResponse,
    already_exists_error_cls=DrawbackSuspensaoAlreadyExistsError,
    not_found_error_cls=DrawbackSuspensaoNotFoundError,
    invalid_state_error_cls=InvalidDrawbackSuspensaoStateError,
)
