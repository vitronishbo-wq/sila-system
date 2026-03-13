from apps.backend.app.modules.public_security.api.endpoints.cadeias_custodia import router as cadeias_custodia_router
from apps.backend.app.modules.public_security.api.endpoints.evidencias import router as evidencias_router
from apps.backend.app.modules.public_security.api.endpoints.investigacoes import router as investigacoes_router
from apps.backend.app.modules.public_security.api.endpoints.laudos_periciais import router as laudos_periciais_router
from apps.backend.app.modules.public_security.api.endpoints.mandados import router as mandados_router
from apps.backend.app.modules.public_security.api.endpoints.ocorrencias import router as ocorrencias_router
from apps.backend.app.modules.public_security.api.endpoints.policiais import router as policiais_router
from apps.backend.app.modules.public_security.api.endpoints.provas_periciais import router as provas_periciais_router
from apps.backend.app.modules.public_security.api.endpoints.unidades_policiais import router as unidades_policiais_router
from apps.backend.app.modules.public_security.api.endpoints.vestigios import router as vestigios_router
__all__ = ['unidades_policiais_router', 'policiais_router', 'ocorrencias_router', 'mandados_router', 'investigacoes_router', 'provas_periciais_router', 'cadeias_custodia_router', 'laudos_periciais_router', 'vestigios_router', 'evidencias_router']