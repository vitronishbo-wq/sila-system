from .atendimento_schema import (
    AtendimentoCreate,
    AtendimentoFinalizacao,
    AtendimentoResponse,
    AtendimentoStatusUpdate,
)
from .bombeiro_schema import BombeiroCreate, BombeiroResponse, BombeiroStatusUpdate
from .corporacao_schema import CorporacaoCreate, CorporacaoResponse, CorporacaoStatusUpdate
from .despacho_schema import DespachoCreate, DespachoResponse, DespachoStatusUpdate
from .ocorrencia_emergencial_schema import (
    OcorrenciaEmergencialCreate,
    OcorrenciaEmergencialResponse,
    OcorrenciaEmergencialStatusUpdate,
)

__all__ = [
    "CorporacaoCreate",
    "CorporacaoResponse",
    "CorporacaoStatusUpdate",
    "BombeiroCreate",
    "BombeiroResponse",
    "BombeiroStatusUpdate",
    "OcorrenciaEmergencialCreate",
    "OcorrenciaEmergencialResponse",
    "OcorrenciaEmergencialStatusUpdate",
    "DespachoCreate",
    "DespachoResponse",
    "DespachoStatusUpdate",
    "AtendimentoCreate",
    "AtendimentoResponse",
    "AtendimentoStatusUpdate",
    "AtendimentoFinalizacao",
]
