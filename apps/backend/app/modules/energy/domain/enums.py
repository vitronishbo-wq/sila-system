"""Energy domain enums"""
from enum import Enum


class FonteEnergia(str, Enum):
    """Tipos de fontes de energia"""
    SOLAR = "solar"
    EOLICA = "eolica"
    HIDROELETRICA = "hidroeletrica"
    TERMOELETRICA = "termoeletrica"
    BIOMASSA = "biomassa"
    NUCLEAR = "nuclear"
    OUTRAS = "outras"


class StatusInfraEnergia(str, Enum):
    """Status da infraestrutura de energia"""
    OPERACIONAL = "operacional"
    EM_MANUTENCAO = "em_manutencao"
    PARADA = "parada"
    DESATIVADA = "desativada"
    DEGRADADA = "degradada"


class TipoLeituraEnergia(str, Enum):
    """Tipos de leitura de energia"""
    REAL = "real"
    ESTIMADA = "estimada"
    CORRIGIDA = "corrigida"
    AJUSTE = "ajuste"


class TipoFatura(str, Enum):
    """Tipos de faturas de energia"""
    NORMAL = "normal"
    ESTIMADA = "estimada"
    CORRIGIDA = "corrigida"
    AJUSTE = "ajuste"


class BandeiraTarifaria(str, Enum):
    """Bandeiras tarifárias"""
    VERDE = "verde"
    AMARELA = "amarela"
    VERMELHA_1 = "vermelha_1"
    VERMELHA_2 = "vermelha_2"


class StatusFaturaEnergia(str, Enum):
    """Status de fatura de energia"""
    RASCUNHO = "rascunho"
    EMITIDA = "emitida"
    PAGA = "paga"
    PENDENTE = "pendente"
    CANCELADA = "cancelada"


class ClasseTensao(str, Enum):
    """Classes de tensão"""
    BAIXA = "baixa"
    MEDIA = "media"
    ALTA = "alta"
    EXTRA_ALTA = "extra_alta"


class StatusUsina(str, Enum):
    """Status operacional da usina"""
    OPERACIONAL = "operacional"
    EM_MANUTENCAO = "em_manutencao"
    CONSTRUCAO = "construcao"
    DESATIVADA = "desativada"


class TipoUsina(str, Enum):
    """Tipos de usina"""
    HIDROELETRICA = "hidroeletrica"
    TERMOELETRICA = "termoeletrica"
    NUCLEAR = "nuclear"
    EOLICA = "eolica"
    SOLAR = "solar"
    BIOMASSA = "biomassa"


__all__ = [
    'FonteEnergia',
    'StatusInfraEnergia',
    'TipoLeituraEnergia',
    'TipoFatura',
    'BandeiraTarifaria',
    'StatusFaturaEnergia',
    'ClasseTensao',
    'StatusUsina',
    'TipoUsina'
]

