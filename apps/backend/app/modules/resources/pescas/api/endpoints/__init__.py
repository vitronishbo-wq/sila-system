from apps.backend.app.modules.resources.pescas.api.endpoints.armadores import router as armadores_router
from apps.backend.app.modules.resources.pescas.api.endpoints.capturas import router as capturas_router
from apps.backend.app.modules.resources.pescas.api.endpoints.comercializacao import router as comercializacao_router
from apps.backend.app.modules.resources.pescas.api.endpoints.defesos import router as defesos_router
from apps.backend.app.modules.resources.pescas.api.endpoints.desembarques import router as desembarques_router
from apps.backend.app.modules.resources.pescas.api.endpoints.embarcacoes import router as embarcacoes_router
from apps.backend.app.modules.resources.pescas.api.endpoints.especies import router as especies_router
from apps.backend.app.modules.resources.pescas.api.endpoints.fiscalizacao import router as fiscalizacao_router
from apps.backend.app.modules.resources.pescas.api.endpoints.licencas_pesca import router as licencas_pesca_router
from apps.backend.app.modules.resources.pescas.api.endpoints.pescadores import router as pescadores_router
from apps.backend.app.modules.resources.pescas.api.endpoints.producao import router as producao_router
from apps.backend.app.modules.resources.pescas.api.endpoints.quotas import router as quotas_router
from apps.backend.app.modules.resources.pescas.api.endpoints.rastreabilidade import router as rastreabilidade_router
__all__ = ['pescadores_router', 'armadores_router', 'embarcacoes_router', 'licencas_pesca_router', 'capturas_router', 'especies_router', 'quotas_router', 'defesos_router', 'desembarques_router', 'producao_router', 'comercializacao_router', 'fiscalizacao_router', 'rastreabilidade_router']