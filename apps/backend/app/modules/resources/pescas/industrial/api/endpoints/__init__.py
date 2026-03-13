from apps.backend.app.modules.resources.pescas.industrial.api.endpoints.armadores_industriais import router as armadores_industriais_router
from apps.backend.app.modules.resources.pescas.industrial.api.endpoints.embarcacoes_industriais import router as embarcacoes_industriais_router
from apps.backend.app.modules.resources.pescas.industrial.api.endpoints.unidades_processamento import router as unidades_processamento_router
from apps.backend.app.modules.resources.pescas.industrial.api.endpoints.frigorificos import router as frigorificos_router
from apps.backend.app.modules.resources.pescas.industrial.api.endpoints.produtos_processados import router as produtos_processados_router
from apps.backend.app.modules.resources.pescas.industrial.api.endpoints.lotes_producao import router as lotes_producao_router
from apps.backend.app.modules.resources.pescas.industrial.api.endpoints.rastreabilidade import router as rastreabilidade_router
from apps.backend.app.modules.resources.pescas.industrial.api.endpoints.certificacoes import router as certificacoes_router
from apps.backend.app.modules.resources.pescas.industrial.api.endpoints.exportacoes_industriais import router as exportacoes_industriais_router
from apps.backend.app.modules.resources.pescas.industrial.api.endpoints.inspecoes_sanitarias import router as inspecoes_sanitarias_router
from apps.backend.app.modules.resources.pescas.industrial.api.endpoints.licencas_operacao import router as licencas_operacao_router
from apps.backend.app.modules.resources.pescas.industrial.api.endpoints.estatisticas import router as estatisticas_router
__all__ = ['armadores_industriais_router', 'embarcacoes_industriais_router', 'unidades_processamento_router', 'frigorificos_router', 'produtos_processados_router', 'lotes_producao_router', 'rastreabilidade_router', 'certificacoes_router', 'exportacoes_industriais_router', 'inspecoes_sanitarias_router', 'licencas_operacao_router', 'estatisticas_router']