from __future__ import annotations
from enum import Enum

class RamoIndustrial(Enum):
    EXTRATIVA = 'extrativa'
    TRANSFORMACAO = 'transformacao'
    ALIMENTAR = 'alimentar'
    BEBIDAS = 'bebidas'
    TEXTIL = 'textil'
    QUIMICA = 'quimica'
    METALURGICA = 'metalurgica'
    ELETRONICA = 'eletronica'
    VEICULOS = 'veiculos'

class PorteIndustrial(Enum):
    MICRO = 'micro'
    PEQUENA = 'pequena'
    MEDIA = 'media'
    GRANDE = 'grande'

class TipoEstabelecimento(Enum):
    MATRIZ = 'matriz'
    FILIAL = 'filial'
    UNIDADE = 'unidade'

class StatusEstabelecimento(Enum):
    ATIVO = 'ativo'
    INATIVO = 'inativo'
    SUSPENSO = 'suspenso'
    LICENCIAMENTO = 'licenciamento'
    CONSTRUCAO = 'construcao'
    PARALISADO = 'paralisado'