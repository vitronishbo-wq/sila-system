from __future__ import annotations

from enum import StrEnum


class TipoAeronave(StrEnum):
    AVIAO = "aviao"
    HELICOPTERO = "helicoptero"
    PLANADOR = "planador"
    ULTRALEVE = "ultraleve"


class CategoriaAeronave(StrEnum):
    TRANSPORTE_PASSAGEIRO = "transporte_passageiro"
    TRANSPORTE_CARGA = "transporte_carga"
    EXECUTIVA = "executiva"
    PARTICULAR = "particular"


class StatusAeronavegabilidade(StrEnum):
    VALIDO = "valido"
    VENCIDO = "vencido"
    SUSPENSO = "suspenso"
    BAIXADA = "baixada"


class TipoVoo(StrEnum):
    REGULAR = "regular"
    NAO_REGULAR = "nao_regular"
    CHARTER = "charter"
    PRIVADO = "privado"
    CARGA = "carga"


class NaturezaVoo(StrEnum):
    DOMESTICO = "domestico"
    INTERNACIONAL = "internacional"


class RegrasVoo(StrEnum):
    VFR = "vfr"
    IFR = "ifr"


class StatusVoo(StrEnum):
    PROGRAMADO = "programado"
    DECOLADO = "decolado"
    EM_VOO = "em_voo"
    POUSADO = "pousado"
    ATRASADO = "atrasado"
    CANCELADO = "cancelado"
    DIVERTIDO = "divertido"


class TipoOcorrencia(StrEnum):
    ACIDENTE = "acidente"
    INCIDENTE = "incidente"
    INCIDENTE_GRAVE = "incidente_grave"


class GravidadeOcorrencia(StrEnum):
    LEVE = "leve"
    MODERADA = "moderada"
    GRAVE = "grave"
    FATAL = "fatal"


class FaseVoo(StrEnum):
    DECOLAGEM = "decolagem"
    CRUZEIRO = "cruzeiro"
    APROXIMACAO = "aproximacao"
    POUSO = "pouso"


class TipoAeroporto(StrEnum):
    INTERNACIONAL = "internacional"
    DOMESTICO = "domestico"
    REGIONAL = "regional"
    PARTICULAR = "particular"
