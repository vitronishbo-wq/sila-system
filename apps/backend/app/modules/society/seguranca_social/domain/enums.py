from __future__ import annotations

from enum import StrEnum


class TipoBeneficiario(StrEnum):
    TRABALHADOR = "trabalhador"
    PENSIONISTA = "pensionista"
    DESEMPREGADO = "desempregado"
    FAMILIA_CARENCIADA = "familia_carenciada"
    IDOSO = "idoso"
    PESSOA_DEFICIENCIA = "pessoa_deficiencia"
    CRIANCA_RISCO = "crianca_risco"
    ESTUDANTE = "estudante"


class RegimeSegurancaSocial(StrEnum):
    GERAL = "geral"
    PUBLICO = "publico"
    AGRICOLA = "agricola"
    DOMESTICO = "domestico"
    INDEPENDENTE = "independente"
    VOLUNTARIO = "voluntario"


class EstadoBeneficiario(StrEnum):
    PENDENTE = "pendente"
    ATIVO = "ativo"
    SUSPENSO = "suspenso"
    CANCELADO = "cancelado"


class TipoPensao(StrEnum):
    VELHICE = "velhice"
    INVALIDEZ = "invalidez"
    SOBREVIVENCIA = "sobrevivencia"
    ORFAO = "orfao"


class StatusPensao(StrEnum):
    AGUARDANDO_APROVACAO = "aguardando_aprovacao"
    ATIVA = "ativa"
    SUSPENSA = "suspensa"
    CANCELADA = "cancelada"


class TipoPrestacao(StrEnum):
    SOCIAL = "social"
    FAMILIAR = "familiar"
    DESEMPREGO = "desemprego"
    DOENCA = "doenca"
    MATERNIDADE = "maternidade"
    PATERNIDADE = "paternidade"
    ADOCAO = "adocao"


class Periodicidade(StrEnum):
    MENSAL = "mensal"
    TRIMESTRAL = "trimestral"
    SEMESTRAL = "semestral"
    ANUAL = "anual"
    UNICA = "unica"
