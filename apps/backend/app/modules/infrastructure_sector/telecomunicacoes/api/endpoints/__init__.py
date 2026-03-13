from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.api.endpoints.assinantes import router as assinantes_router
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.api.endpoints.espectros import router as espectros_router
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.api.endpoints.faturas import router as faturas_router
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.api.endpoints.indicadores_qualidade import router as indicadores_qualidade_router
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.api.endpoints.infraestruturas import router as infraestruturas_router
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.api.endpoints.operadoras import router as operadoras_router
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.api.endpoints.outorgas_espectro import router as outorgas_espectro_router
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.api.endpoints.qualidade_servico import router as qualidade_servico_router
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.api.endpoints.reclamacoes import router as reclamacoes_router
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.api.endpoints.slas import router as slas_router
__all__ = ['operadoras_router', 'assinantes_router', 'faturas_router', 'reclamacoes_router', 'infraestruturas_router', 'outorgas_espectro_router', 'espectros_router', 'slas_router', 'qualidade_servico_router', 'indicadores_qualidade_router']