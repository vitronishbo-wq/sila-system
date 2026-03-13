from __future__ import annotations
from enum import Enum

class TipoAeronave(str, Enum):
    AVIAO = 'aviao'
    HELICOPTERO = 'helicoptero'
    PLANADOR = 'planador'
    ULTRALEVE = 'ultraleve'

class CategoriaAeronave(str, Enum):
    TRANSPORTE_PASSAGEIRO = 'transporte_passageiro'
    TRANSPORTE_CARGA = 'transporte_carga'
    EXECUTIVA = 'executiva'
    PARTICULAR = 'particular'

class StatusAeronavegabilidade(str, Enum):
    VALIDO = 'valido'
    VENCIDO = 'vencido'
    SUSPENSO = 'suspenso'
    BAIXADA = 'baixada'

class TipoVoo(str, Enum):
    REGULAR = 'regular'
    NAO_REGULAR = 'nao_regular'
    CHARTER = 'charter'
    PRIVADO = 'privado'
    CARGA = 'carga'

class NaturezaVoo(str, Enum):
    DOMESTICO = 'domestico'
    INTERNACIONAL = 'internacional'

class RegrasVoo(str, Enum):
    VFR = 'vfr'
    IFR = 'ifr'

class StatusVoo(str, Enum):
    PROGRAMADO = 'programado'
    DECOLADO = 'decolado'
    EM_VOO = 'em_voo'
    POUSADO = 'pousado'
    ATRASADO = 'atrasado'
    CANCELADO = 'cancelado'
    DIVERTIDO = 'divertido'

class TipoOcorrencia(str, Enum):
    ACIDENTE = 'acidente'
    INCIDENTE = 'incidente'
    INCIDENTE_GRAVE = 'incidente_grave'

class GravidadeOcorrencia(str, Enum):
    LEVE = 'leve'
    MODERADA = 'moderada'
    GRAVE = 'grave'
    FATAL = 'fatal'

class FaseVoo(str, Enum):
    DECOLAGEM = 'decolagem'
    CRUZEIRO = 'cruzeiro'
    APROXIMACAO = 'aproximacao'
    POUSO = 'pouso'

class TipoAeroporto(str, Enum):
    INTERNACIONAL = 'internacional'
    DOMESTICO = 'domestico'
    REGIONAL = 'regional'
    PARTICULAR = 'particular'