from apps.backend.app.modules.society.assistencia_social.api.endpoints.atendimentos import (
    router as atendimentos_router,
)
from apps.backend.app.modules.society.assistencia_social.api.endpoints.beneficiarios import (
    router as beneficiarios_router,
)
from apps.backend.app.modules.society.assistencia_social.api.endpoints.beneficios import (
    router as beneficios_router,
)
from apps.backend.app.modules.society.assistencia_social.api.endpoints.cadastros_unicos import (
    router as cadastros_unicos_router,
)
from apps.backend.app.modules.society.assistencia_social.api.endpoints.criancas_risco import (
    router as criancas_risco_router,
)
from apps.backend.app.modules.society.assistencia_social.api.endpoints.idosos_vulneraveis import (
    router as idosos_vulneraveis_router,
)
from apps.backend.app.modules.society.assistencia_social.api.endpoints.pcd import (
    router as pcd_router,
)
from apps.backend.app.modules.society.assistencia_social.api.endpoints.programas_sociais import (
    router as programas_sociais_router,
)
from apps.backend.app.modules.society.assistencia_social.api.endpoints.situacoes_rua import (
    router as situacoes_rua_router,
)
from apps.backend.app.modules.society.assistencia_social.api.endpoints.visitas_domiciliares import (
    router as visitas_domiciliares_router,
)

__all__ = [
    "atendimentos_router",
    "beneficiarios_router",
    "beneficios_router",
    "cadastros_unicos_router",
    "criancas_risco_router",
    "idosos_vulneraveis_router",
    "pcd_router",
    "programas_sociais_router",
    "situacoes_rua_router",
    "visitas_domiciliares_router",
]
