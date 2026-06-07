from __future__ import annotations

from enum import StrEnum


class TipoAcordo(StrEnum):
    TRATADO = "tratado"
    CONVENIO = "convenio"
    PROTOCOLO = "protocolo"
    MEMORANDO = "memorando"
    DECLARACAO_CONJUNTA = "declaracao_conjunta"


class StatusAcordo(StrEnum):
    NEGOCIACAO = "negociacao"
    ASSINADO = "assinado"
    RATIFICADO = "ratificado"
    EM_VIGOR = "em_vigor"
    SUSPENSO = "suspenso"
    EXTINTO = "extinto"


class NaturezaJuridica(StrEnum):
    VINCULANTE = "vinculante"
    NAO_VINCULANTE = "nao_vinculante"
    MISTO = "misto"


class TipoProjeto(StrEnum):
    COOPERACAO_TECNICA = "cooperacao_tecnica"
    COOPERACAO_CIENTIFICA = "cooperacao_cientifica"
    COOPERACAO_EDUCACIONAL = "cooperacao_educacional"
    COOPERACAO_HUMANITARIA = "cooperacao_humanitaria"


class ModalidadeCooperacao(StrEnum):
    BILATERAL = "bilateral"
    MULTILATERAL = "multilateral"
    REGIONAL = "regional"
    TRIANGULAR = "triangular"


class StatusProjeto(StrEnum):
    PROPOSTA = "proposta"
    APROVADO = "aprovado"
    EM_EXECUCAO = "em_execucao"
    CONCLUIDO = "concluido"
    CANCELADO = "cancelado"


class TipoVisto(StrEnum):
    DIPLOMATICO = "diplomatico"
    OFICIAL = "oficial"
    CORTESIA = "cortesia"
    TRABALHO = "trabalho"
    ESTUDANTE = "estudante"


class CategoriaVisto(StrEnum):
    VITEM_I = "vitem_i"
    VITEM_II = "vitem_ii"
    VITEM_IV = "vitem_iv"
    VITEM_V = "vitem_v"
    VIPER = "viper"


class StatusVisto(StrEnum):
    SOLICITADO = "solicitado"
    EM_ANALISE = "em_analise"
    APROVADO = "aprovado"
    NEGADO = "negado"
    EMITIDO = "emitido"
    VENCIDO = "vencido"
    CANCELADO = "cancelado"
