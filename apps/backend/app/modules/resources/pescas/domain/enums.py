from __future__ import annotations
from enum import Enum

class TipoPescador(str, Enum):
    ARTESANAL = 'artesanal'
    INDUSTRIAL = 'industrial'
    DESPORTIVO = 'desportivo'
    CIENTIFICO = 'cientifico'

class TipoEmbarcacao(str, Enum):
    ARTESANAL = 'artesanal'
    INDUSTRIAL = 'industrial'
    APOIO = 'apoio'
    PESQUISA = 'pesquisa'

class ModalidadePesca(str, Enum):
    ARRASTO = 'arrasto'
    CERCO = 'cerco'
    ESPINHEL = 'espinhel'
    REDE_EMALHE = 'rede_emalhe'
    LINHA_MAO = 'linha_mao'
    COVO = 'covo'
    MERGULHO = 'mergulho'
    TARRAFA = 'tarrafa'

class StatusLicenca(str, Enum):
    REQUERIDA = 'requerida'
    EM_ANALISE = 'em_analise'
    DEFERIDA = 'deferida'
    INDEFERIDA = 'indeferida'
    VENCIDA = 'vencida'
    SUSPENSA = 'suspensa'
    CANCELADA = 'cancelada'

class PeriodoDefesoTipo(str, Enum):
    ANDROVIA = 'androvia'
    CAMARAO = 'camarao'
    LAGOSTA = 'lagosta'
    PESCADA = 'pescada'
    CORVINA = 'corvina'
    SARDINHA = 'sardinha'