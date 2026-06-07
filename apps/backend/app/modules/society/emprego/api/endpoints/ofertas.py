from apps.backend.app.modules.society.emprego.api.deps import get_oferta_service
from apps.backend.app.modules.society.emprego.api.endpoints._workflow_endpoints import (
    build_workflow_router,
)
from apps.backend.app.modules.society.emprego.api.schemas.oferta_schema import (
    OfertaAction,
    OfertaCancel,
    OfertaCreate,
    OfertaResponse,
)

router = build_workflow_router(
    tag="Emprego - Ofertas",
    get_service=get_oferta_service,
    create_schema=OfertaCreate,
    action_schema=OfertaAction,
    cancel_schema=OfertaCancel,
    response_schema=OfertaResponse,
    routes=[("/ofertas", "oferta_emprego")],
)
