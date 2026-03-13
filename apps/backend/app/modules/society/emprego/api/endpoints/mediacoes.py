from app.modules.society.emprego.api.deps import get_mediacao_service
from app.modules.society.emprego.api.endpoints._workflow_endpoints import build_workflow_router
from app.modules.society.emprego.api.schemas.mediacao_schema import MediacaoAction, MediacaoCancel, MediacaoCreate, MediacaoResponse
router = build_workflow_router(tag='Emprego - Mediacao', get_service=get_mediacao_service, create_schema=MediacaoCreate, action_schema=MediacaoAction, cancel_schema=MediacaoCancel, response_schema=MediacaoResponse, routes=[('/mediacoes', 'mediacao'), ('/mediacoes/emprego', 'mediacao_emprego')])