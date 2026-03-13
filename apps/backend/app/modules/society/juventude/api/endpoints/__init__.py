from apps.backend.app.modules.society.juventude.api.endpoints.acompanhamentos import router as acompanhamentos_router
from apps.backend.app.modules.society.juventude.api.endpoints.auxilios import router as auxilios_router
from apps.backend.app.modules.society.juventude.api.endpoints.bolsas_estudo import router as bolsas_estudo_router
from apps.backend.app.modules.society.juventude.api.endpoints.empreendedorismo_juvenil import router as empreendedorismo_juvenil_router
from apps.backend.app.modules.society.juventude.api.endpoints.estagios import router as estagios_router
from apps.backend.app.modules.society.juventude.api.endpoints.eventos_juvenis import router as eventos_juvenis_router
from apps.backend.app.modules.society.juventude.api.endpoints.formacoes import router as formacoes_router
from apps.backend.app.modules.society.juventude.api.endpoints.inscricoes_programa import router as inscricoes_programa_router
from apps.backend.app.modules.society.juventude.api.endpoints.intercambios import router as intercambios_router
from apps.backend.app.modules.society.juventude.api.endpoints.jovens import router as jovens_router
from apps.backend.app.modules.society.juventude.api.endpoints.mentores import router as mentores_router
from apps.backend.app.modules.society.juventude.api.endpoints.politicas_juventude import router as politicas_juventude_router
from apps.backend.app.modules.society.juventude.api.endpoints.programas import router as programas_router
from apps.backend.app.modules.society.juventude.api.endpoints.risco_evasao import router as risco_evasao_router
from apps.backend.app.modules.society.juventude.api.endpoints.saude_juvenil import router as saude_juvenil_router
from apps.backend.app.modules.society.juventude.api.endpoints.voluntariados import router as voluntariados_router
from apps.backend.app.modules.society.juventude.api.endpoints._workflow_endpoints import build_workflow_router
__all__ = ['acompanhamentos_router', 'jovens_router', 'auxilios_router', 'programas_router', 'formacoes_router', 'bolsas_estudo_router', 'estagios_router', 'inscricoes_programa_router', 'intercambios_router', 'mentores_router', 'eventos_juvenis_router', 'voluntariados_router', 'empreendedorismo_juvenil_router', 'saude_juvenil_router', 'politicas_juventude_router', 'risco_evasao_router', 'build_workflow_router']