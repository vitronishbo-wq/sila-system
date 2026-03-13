from __future__ import annotations
from enum import Enum

class TipoOperadorFlorestal(Enum):
    EMPRESA = 'empresa'
    COMUNIDADE = 'comunidade'
    COOPERATIVA = 'cooperativa'
    ASSENTAMENTO = 'assentamento'
    CONCESSIONARIO = 'concessionario'

class TipoManejo(Enum):
    SUSTENTAVEL = 'sustentavel'
    CONVENCIONAL = 'convencional'
    COMUNITARIO = 'comunitario'

class StatusPlanoManejo(Enum):
    ELABORACAO = 'elaboracao'
    SUBMETIDO = 'submetido'
    EM_ANALISE = 'em_analise'
    APROVADO = 'aprovado'
    REPROVADO = 'reprovado'
    EM_EXECUCAO = 'em_execucao'
    CONCLUIDO = 'concluido'
    SUSPENSO = 'suspenso'
    CANCELADO = 'cancelado'

class TipoCicloCorte(Enum):
    ANUAL = 'anual'
    BIENAL = 'bienal'
    QUINQUENAL = 'quinquenal'
    DECENAL = 'decenal'

class TipoProdutoFlorestal(Enum):
    MADEIRA_TORA = 'madeira_tora'
    MADEIRA_SERRADA = 'madeira_serrada'
    LAMINADO = 'laminado'
    COMPENSADO = 'compensado'
    CARVAO = 'carvao'
    LENHA = 'lenha'
    CASTANHA = 'castanha'
    BORRACHA = 'borracha'
    RESINA = 'resina'
    OLEO_ESSENCIAL = 'oleo_essencial'
    PLANTA_MEDICINAL = 'planta_medicinal'
    FRUTO = 'fruto'

class StatusDOF(Enum):
    EMITIDA = 'emitida'
    UTILIZADA = 'utilizada'
    CANCELADA = 'cancelada'
    VENCIDA = 'vencida'

class TipoFocoCalor(Enum):
    SATELITE = 'satelite'
    AEREO = 'aereo'
    TERRESTRE = 'terrestre'
    DENUNCIA = 'denuncia'

class TipoAlertaDesmatamento(Enum):
    PRODES = 'prodes'
    DETER = 'deter'
    SAD = 'sad'
    GLAD = 'glad'
    DENUNCIA = 'denuncia'

class TipoCreditoCarbono(Enum):
    REDD = 'redd'
    REDD_PLUS = 'redd_plus'
    ARR = 'arr'
    IFM = 'ifm'
    ALM = 'alm'