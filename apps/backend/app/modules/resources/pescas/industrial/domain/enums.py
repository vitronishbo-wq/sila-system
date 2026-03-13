from enum import Enum

class TipoProcessamento(str, Enum):
    FILETAGEM = 'filetagem'
    CONSERVA = 'conserva'
    ENLATADO = 'enlatado'
    CONGELADO = 'congelado'
    SECO = 'seco'
    SALGADO = 'salgado'
    DEFUMADO = 'defumado'
    FARINHA = 'farinha'
    OLEO = 'oleo'

class TipoProdutoProcessado(str, Enum):
    FILETE = 'filete'
    POSTA = 'posta'
    CONSERVA = 'conserva'
    ENLATADO = 'enlatado'
    CONGELADO = 'congelado'
    SECO = 'seco'
    SALGADO = 'salgado'
    DEFUMADO = 'defumado'
    FARINHA = 'farinha'
    OLEO = 'oleo'
    SUBPRODUTO = 'subproduto'

class ClassificacaoIndustrial(str, Enum):
    TIPO_A = 'tipo_a'
    TIPO_B = 'tipo_b'
    TIPO_C = 'tipo_c'

class StatusInspecao(str, Enum):
    AGENDADA = 'agendada'
    EM_ANDAMENTO = 'em_andamento'
    APROVADA = 'aprovada'
    REPROVADA = 'reprovada'
    PENDENCIA = 'pendencia'
    INTERDITADA = 'interditada'

class TipoSeloInspecao(str, Enum):
    SIF = 'sif'
    SIE = 'sie'
    SIM = 'sim'

class StatusLoteProducao(str, Enum):
    ABERTO = 'aberto'
    EM_PROCESSAMENTO = 'em_processamento'
    CONCLUIDO = 'concluido'
    BLOQUEADO = 'bloqueado'
    DESCARTADO = 'descartado'

class MercadoDestino(str, Enum):
    INTERNO = 'interno'
    EXPORTACAO = 'exportacao'