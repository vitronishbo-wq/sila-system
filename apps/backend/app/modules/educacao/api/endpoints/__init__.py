from .boletins import router as boletins_router
from .certificados import router as certificados_router
from .concursos import router as concursos_router
from .emprego import router as emprego_router
from .formacoes import router as formacoes_router
from .inscricoes import router as inscricoes_router
from .matricula_routes import router as matricula_router
from .propinas import router as propinas_router
from .transferencias import router as transferencias_router
from .universidade import router as universidade_router

__all__ = [
    "matricula_router",
    "inscricoes_router",
    "boletins_router",
    "certificados_router",
    "transferencias_router",
    "propinas_router",
    "emprego_router",
    "concursos_router",
    "formacoes_router",
    "universidade_router",
]
