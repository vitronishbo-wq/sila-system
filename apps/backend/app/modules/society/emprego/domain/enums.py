from __future__ import annotations

from enum import StrEnum


class Escolaridade(StrEnum):
    SEM_ESCOLARIDADE = "sem_escolaridade"
    BASICA = "basica"
    SECUNDARIA = "secundaria"
    TECNICA = "tecnica"
    SUPERIOR = "superior"
    POS_GRADUACAO = "pos_graduacao"


class SituacaoProfissional(StrEnum):
    EMPREGADO = "empregado"
    DESEMPREGADO = "desempregado"
    PRIMEIRO_EMPREGO = "primeiro_emprego"
    AUTONOMO = "autonomo"
    ESTAGIARIO = "estagiario"


class StatusCandidato(StrEnum):
    ATIVO = "ativo"
    COLOCADO = "colocado"
    INATIVO = "inativo"
    SUSPENSO = "suspenso"


class WorkflowStatus(StrEnum):
    PENDENTE = "pendente"
    EM_ANALISE = "em_analise"
    APROVADA = "aprovada"
    REJEITADA = "rejeitada"
    CONCLUIDA = "concluida"
    CANCELADA = "cancelada"
