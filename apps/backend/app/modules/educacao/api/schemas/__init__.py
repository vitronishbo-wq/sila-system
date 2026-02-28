from .escola_schema import EscolaResponse
from .inscricao_schema import (
    InscricaoCancelar,
    InscricaoConfirmar,
    InscricaoCreate,
    InscricaoResponse,
)
from .matricula_schema import MatriculaAtivar, MatriculaCreate, MatriculaListFilter, MatriculaResponse

__all__ = [
    "MatriculaCreate",
    "MatriculaAtivar",
    "MatriculaResponse",
    "MatriculaListFilter",
    "EscolaResponse",
    "InscricaoCreate",
    "InscricaoConfirmar",
    "InscricaoCancelar",
    "InscricaoResponse",
]
