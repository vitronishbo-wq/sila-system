from __future__ import annotations

from enum import StrEnum


class StatusFluxo(StrEnum):
    PENDENTE = "pendente"
    CONFIRMADA = "confirmada"
    EM_ANALISE = "em_analise"
    APROVADA = "aprovada"
    REJEITADA = "rejeitada"
    CONCLUIDA = "concluida"
    CANCELADA = "cancelada"


class TipoInscricao(StrEnum):
    BASICA = "basica"
    SECUNDARIA = "secundaria"
    SUPERIOR = "superior"
    TECNICO = "tecnico"
