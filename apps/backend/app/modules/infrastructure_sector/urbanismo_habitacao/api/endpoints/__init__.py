from app.modules.infrastructure_sector.urbanismo_habitacao.api.endpoints.alvaras import router as alvaras_router
from app.modules.infrastructure_sector.urbanismo_habitacao.api.endpoints.habitese import router as habitese_router
from app.modules.infrastructure_sector.urbanismo_habitacao.api.endpoints.licencas_urbanisticas import router as licencas_urbanisticas_router
from app.modules.infrastructure_sector.urbanismo_habitacao.api.endpoints.loteamentos import router as loteamentos_router
from app.modules.infrastructure_sector.urbanismo_habitacao.api.endpoints.operacoes_urbanas import router as operacoes_urbanas_router
from app.modules.infrastructure_sector.urbanismo_habitacao.api.endpoints.parcelamentos import router as parcelamentos_router
from app.modules.infrastructure_sector.urbanismo_habitacao.api.endpoints.planos_diretores import router as planos_diretores_router
from app.modules.infrastructure_sector.urbanismo_habitacao.api.endpoints.zoneamento import router as zoneamento_router
__all__ = ['planos_diretores_router', 'zoneamento_router', 'operacoes_urbanas_router', 'parcelamentos_router', 'loteamentos_router', 'licencas_urbanisticas_router', 'alvaras_router', 'habitese_router']