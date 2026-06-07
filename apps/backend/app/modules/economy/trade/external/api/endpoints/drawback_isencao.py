from apps.backend.app.modules.economy.trade.external.api.deps import (
    get_drawback_isencao_service_protected,
)
from apps.backend.app.modules.economy.trade.external.api.endpoints._habilitacao_router import (
    build_habilitacao_router,
)
from apps.backend.app.modules.economy.trade.external.api.schemas.drawback_isencao_schema import (
    DrawbackIsencaoAprovacaoInput,
    DrawbackIsencaoCreate,
    DrawbackIsencaoRejeicaoInput,
    DrawbackIsencaoResponse,
)
from apps.backend.app.modules.economy.trade.external.exceptions import (
    DrawbackIsencaoAlreadyExistsError,
    DrawbackIsencaoNotFoundError,
    InvalidDrawbackIsencaoStateError,
)

router = build_habilitacao_router(
    prefix="/drawback_isencao",
    tag="Comercio Externo - Drawback Isencao",
    get_service=get_drawback_isencao_service_protected,
    create_schema=DrawbackIsencaoCreate,
    aprovacao_schema=DrawbackIsencaoAprovacaoInput,
    rejeicao_schema=DrawbackIsencaoRejeicaoInput,
    response_schema=DrawbackIsencaoResponse,
    already_exists_error_cls=DrawbackIsencaoAlreadyExistsError,
    not_found_error_cls=DrawbackIsencaoNotFoundError,
    invalid_state_error_cls=InvalidDrawbackIsencaoStateError,
)
