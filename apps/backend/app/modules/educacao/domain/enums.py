from __future__ import annotations

from enum import Enum


class StatusFluxo(str, Enum):
    PENDENTE = "pendente"
    CONFIRMADA = "confirmada"
    EM_ANALISE = "em_analise"
    APROVADA = "aprovada"
    REJEITADA = "rejeitada"
    CONCLUIDA = "concluida"
    CANCELADA = "cancelada"


class TipoInscricao(str, Enum):
    BASICA = "basica"
    SECUNDARIA = "secundaria"
    SUPERIOR = "superior"
    TECNICO = "tecnico"
