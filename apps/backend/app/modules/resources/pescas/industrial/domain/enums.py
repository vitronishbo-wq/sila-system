from enum import StrEnum


class TipoProcessamento(StrEnum):
    FILETAGEM = "filetagem"
    CONSERVA = "conserva"
    ENLATADO = "enlatado"
    CONGELADO = "congelado"
    SECO = "seco"
    SALGADO = "salgado"
    DEFUMADO = "defumado"
    FARINHA = "farinha"
    OLEO = "oleo"


class TipoProdutoProcessado(StrEnum):
    FILETE = "filete"
    POSTA = "posta"
    CONSERVA = "conserva"
    ENLATADO = "enlatado"
    CONGELADO = "congelado"
    SECO = "seco"
    SALGADO = "salgado"
    DEFUMADO = "defumado"
    FARINHA = "farinha"
    OLEO = "oleo"
    SUBPRODUTO = "subproduto"


class ClassificacaoIndustrial(StrEnum):
    TIPO_A = "tipo_a"
    TIPO_B = "tipo_b"
    TIPO_C = "tipo_c"


class StatusInspecao(StrEnum):
    AGENDADA = "agendada"
    EM_ANDAMENTO = "em_andamento"
    APROVADA = "aprovada"
    REPROVADA = "reprovada"
    PENDENCIA = "pendencia"
    INTERDITADA = "interditada"


class TipoSeloInspecao(StrEnum):
    SIF = "sif"
    SIE = "sie"
    SIM = "sim"


class StatusLoteProducao(StrEnum):
    ABERTO = "aberto"
    EM_PROCESSAMENTO = "em_processamento"
    CONCLUIDO = "concluido"
    BLOQUEADO = "bloqueado"
    DESCARTADO = "descartado"


class MercadoDestino(StrEnum):
    INTERNO = "interno"
    EXPORTACAO = "exportacao"
