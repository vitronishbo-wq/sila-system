from enum import Enum

class TipoImovel(Enum):
    URBANO = 'urbano'
    RURAL = 'rural'
    MISTO = 'misto'
    TERRENO = 'terreno'
    EDIFICACAO = 'edificacao'
    CASA = 'casa'
    APARTAMENTO = 'apartamento'
    SALA = 'sala'
    LOJA = 'loja'
    GALPAO = 'galpao'
    TELHEIRO = 'telheiro'
    SITIO = 'sitio'
    CHACARA = 'chacara'
    FAZENDA = 'fazenda'
    GLEBA = 'gleba'
    LOTE = 'lote'
    QUADRA = 'quadra'

class NaturezaImovel(Enum):
    PUBLICO = 'publico'
    PRIVADO = 'privado'
    MISTO = 'misto'
    DEVOLUTO = 'devoluto'
    OCUPADO = 'ocupado'

class RegimePropriedade(Enum):
    PLENA = 'plena'
    LIMITADA = 'limitada'
    CONDOMINIO = 'condominio'
    COOPERATIVA = 'cooperativa'
    COMODATO = 'comodato'
    CONCESSAO = 'concessao'
    ENFITEUSE = 'enfiteuse'
    POSSE = 'posse'

class TipoOcupacao(Enum):
    PROPRIETARIO = 'proprietario'
    POSSUIDOR = 'possuidor'
    DETENTOR = 'detentor'
    LOCATARIO = 'locatario'
    COMODATARIO = 'comodatario'
    CESSIONARIO = 'cessionario'
    OCUPANTE = 'ocupante'

class SituacaoDominial(Enum):
    REGULAR = 'regular'
    IRREGULAR = 'irregular'
    EM_REGULARIZACAO = 'em_regularizacao'
    LITIGIOSO = 'litigioso'
    USUCAPIAO = 'usucapiao'
    POSSE = 'posse'
    OCUPACAO = 'ocupacao'

class TipoRegistro(Enum):
    MATRICULA = 'matricula'
    TRANSCRICAO = 'transcricao'
    INSCRICAO = 'inscricao'
    AVERBACAO = 'averbacao'
    REGISTRO = 'registro'

class StatusMatriculaImovel(Enum):
    ATIVA = 'ativa'
    CANCELADA = 'cancelada'
    TRANSFERIDA = 'transferida'

class TipoAlienacao(Enum):
    VENDA = 'venda'
    PERMUTA = 'permuta'
    DOACAO = 'doacao'
    DACAO_PAGAMENTO = 'dacao_pagamento'
    HERANCA = 'heranca'
    LEGADO = 'legado'
    USUCAPIAO = 'usucapiao'
    DESAPROPRIACAO = 'desapropriacao'

class TipoDesapropriacao(Enum):
    UTILIDADE_PUBLICA = 'utilidade_publica'
    INTERESSE_SOCIAL = 'interesse_social'
    SANEAMENTO = 'saneamento'
    REFORMA_AGRARIA = 'reforma_agraria'

class StatusDesapropriacao(Enum):
    INSTAURADA = 'instaurada'
    EM_AVALIACAO = 'em_avaliacao'
    DECRETADA = 'decretada'
    INDENIZADA = 'indenizada'
    ENCERRADA = 'encerrada'
    CANCELADA = 'cancelada'

class TipoOneracao(Enum):
    HIPOTECA = 'hipoteca'
    PENHORA = 'penhora'
    ALIENACAO_FIDUCIARIA = 'alienacao_fiduciaria'
    USUFRUTO = 'usufruto'
    SERVIDAO = 'servidao'

class StatusOneracao(Enum):
    ATIVA = 'ativa'
    BAIXADA = 'baixada'
    CANCELADA = 'cancelada'

class TipoReurb(Enum):
    INTERESSE_SOCIAL = 'interesse_social'
    ESPECIFICO = 'especifico'

class StatusReurb(Enum):
    PROTOCOLADA = 'protocolada'
    EM_ANALISE = 'em_analise'
    APROVADA = 'aprovada'
    IMPUGNADA = 'impugnada'
    ARQUIVADA = 'arquivada'
    CONCLUIDA = 'concluida'

class TipoPessoa(Enum):
    SINGULAR = 'singular'
    COLETIVA = 'coletiva'

class TipoTitularidade(Enum):
    PROPRIETARIO = 'proprietario'
    TITULAR = 'titular'
    COTITULAR = 'cotitular'
    USUFRUTUARIO = 'usufrutuario'