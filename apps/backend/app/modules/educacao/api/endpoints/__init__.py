from .boletins import router as boletins_router
from .certificados import router as certificados_router
from .concursos import router as concursos_router
from .emprego import router as emprego_router
from .formacoes import router as formacoes_router
from .inscricoes import router as inscricoes_router
from .matricula_routes import router as matricula_router
from .propinas import router as propinas_router
from .transferencias import router as transferencias_router
from .transferencias_automacao import router as transferencias_automacao_router
from .universidade import router as universidade_router
from .marketplace_endpoints import router as marketplace_router
from .transfer_wizard import router as transfer_wizard_router
from .metrics_endpoints import router as metrics_router
from .wizard_matricula import router as wizard_matricula_router
from ...emis.api.endpoints import router as emis_router
from .academic_identity import router as academic_identity_router
from .academic_wallet import router as academic_wallet_router
from .escolas_routes import router as escolas_router
from .turmas_routes import router as turmas_router
from .fuc_routes import router as fuc_router

__all__ = [
    "marketplace_router",
    "metrics_router",
    "transfer_wizard_router",
    "matricula_router",
    "inscricoes_router",
    "boletins_router",
    "certificados_router",
    "transferencias_router",
    "transferencias_automacao_router",
    "propinas_router",
    "emprego_router",
    "concursos_router",
    "formacoes_router",
    "universidade_router",
    "wizard_matricula_router",
    "emis_router",
    "academic_identity_router",
    "academic_wallet_router",
    "escolas_router",
    "turmas_router",
    "fuc_router",
]
