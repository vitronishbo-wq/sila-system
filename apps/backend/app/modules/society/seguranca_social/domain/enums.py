from __future__ import annotations
from enum import Enum

class TipoBeneficiario(str, Enum):
    TRABALHADOR = 'trabalhador'
    PENSIONISTA = 'pensionista'
    DESEMPREGADO = 'desempregado'
    FAMILIA_CARENCIADA = 'familia_carenciada'
    IDOSO = 'idoso'
    PESSOA_DEFICIENCIA = 'pessoa_deficiencia'
    CRIANCA_RISCO = 'crianca_risco'
    ESTUDANTE = 'estudante'

class RegimeSegurancaSocial(str, Enum):
    GERAL = 'geral'
    PUBLICO = 'publico'
    AGRICOLA = 'agricola'
    DOMESTICO = 'domestico'
    INDEPENDENTE = 'independente'
    VOLUNTARIO = 'voluntario'

class EstadoBeneficiario(str, Enum):
    PENDENTE = 'pendente'
    ATIVO = 'ativo'
    SUSPENSO = 'suspenso'
    CANCELADO = 'cancelado'

class TipoPensao(str, Enum):
    VELHICE = 'velhice'
    INVALIDEZ = 'invalidez'
    SOBREVIVENCIA = 'sobrevivencia'
    ORFAO = 'orfao'

class StatusPensao(str, Enum):
    AGUARDANDO_APROVACAO = 'aguardando_aprovacao'
    ATIVA = 'ativa'
    SUSPENSA = 'suspensa'
    CANCELADA = 'cancelada'

class TipoPrestacao(str, Enum):
    SOCIAL = 'social'
    FAMILIAR = 'familiar'
    DESEMPREGO = 'desemprego'
    DOENCA = 'doenca'
    MATERNIDADE = 'maternidade'
    PATERNIDADE = 'paternidade'
    ADOCAO = 'adocao'

class Periodicidade(str, Enum):
    MENSAL = 'mensal'
    TRIMESTRAL = 'trimestral'
    SEMESTRAL = 'semestral'
    ANUAL = 'anual'
    UNICA = 'unica'