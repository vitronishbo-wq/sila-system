from apps.backend.app.modules.economy.trade.external.api.deps import (
    get_habilitacao_importador_service,
)
from apps.backend.app.modules.economy.trade.external.api.endpoints._habilitacao_router import (
    build_habilitacao_router,
)
from apps.backend.app.modules.economy.trade.external.api.schemas.habilitacao_importador_schema import (
    HabilitacaoImportadorAprovacaoInput,
    HabilitacaoImportadorCreate,
    HabilitacaoImportadorRejeicaoInput,
    HabilitacaoImportadorResponse,
)
from apps.backend.app.modules.economy.trade.external.exceptions import (
    HabilitacaoImportadorAlreadyExistsError,
    HabilitacaoImportadorNotFoundError,
    InvalidHabilitacaoImportadorStateError,
)

router = build_habilitacao_router(
    prefix="/habilitacoes-importador",
    tag="Comercio Externo - Habilitacoes Importador",
    get_service=get_habilitacao_importador_service,
    create_schema=HabilitacaoImportadorCreate,
    aprovacao_schema=HabilitacaoImportadorAprovacaoInput,
    rejeicao_schema=HabilitacaoImportadorRejeicaoInput,
    response_schema=HabilitacaoImportadorResponse,
    already_exists_error_cls=HabilitacaoImportadorAlreadyExistsError,
    not_found_error_cls=HabilitacaoImportadorNotFoundError,
    invalid_state_error_cls=InvalidHabilitacaoImportadorStateError,
)
