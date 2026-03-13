from __future__ import annotations
from enum import Enum

class Escolaridade(str, Enum):
    SEM_ESCOLARIDADE = 'sem_escolaridade'
    BASICA = 'basica'
    SECUNDARIA = 'secundaria'
    TECNICA = 'tecnica'
    SUPERIOR = 'superior'
    POS_GRADUACAO = 'pos_graduacao'

class SituacaoProfissional(str, Enum):
    EMPREGADO = 'empregado'
    DESEMPREGADO = 'desempregado'
    PRIMEIRO_EMPREGO = 'primeiro_emprego'
    AUTONOMO = 'autonomo'
    ESTAGIARIO = 'estagiario'

class StatusCandidato(str, Enum):
    ATIVO = 'ativo'
    COLOCADO = 'colocado'
    INATIVO = 'inativo'
    SUSPENSO = 'suspenso'

class WorkflowStatus(str, Enum):
    PENDENTE = 'pendente'
    EM_ANALISE = 'em_analise'
    APROVADA = 'aprovada'
    REJEITADA = 'rejeitada'
    CONCLUIDA = 'concluida'
    CANCELADA = 'cancelada'