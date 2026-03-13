from __future__ import annotations
from apps.backend.app.modules.industry.domain.enums import PorteIndustrial, RamoIndustrial
from apps.backend.app.modules.industry.domain.models.porte_industrial import Porte
from apps.backend.app.modules.industry.domain.models.ramo_industrial import Ramo
RAMOS_CATALOG: dict[RamoIndustrial, str] = {RamoIndustrial.EXTRATIVA: 'Industria extrativa', RamoIndustrial.TRANSFORMACAO: 'Industria de transformacao', RamoIndustrial.ALIMENTAR: 'Industria alimentar', RamoIndustrial.BEBIDAS: 'Industria de bebidas', RamoIndustrial.TEXTIL: 'Industria textil', RamoIndustrial.QUIMICA: 'Industria quimica', RamoIndustrial.METALURGICA: 'Industria metalurgica', RamoIndustrial.ELETRONICA: 'Industria eletronica', RamoIndustrial.VEICULOS: 'Industria de veiculos'}
PORTES_CATALOG: dict[PorteIndustrial, str] = {PorteIndustrial.MICRO: 'Micro industria', PorteIndustrial.PEQUENA: 'Pequena industria', PorteIndustrial.MEDIA: 'Media industria', PorteIndustrial.GRANDE: 'Grande industria'}

def get_ramo(codigo: RamoIndustrial) -> Ramo:
    return Ramo(codigo=codigo, descricao=RAMOS_CATALOG[codigo])

def get_porte(codigo: PorteIndustrial) -> Porte:
    return Porte(codigo=codigo, descricao=PORTES_CATALOG[codigo])

def list_ramos() -> list[Ramo]:
    return [get_ramo(codigo) for codigo in RAMOS_CATALOG]

def list_portes() -> list[Porte]:
    return [get_porte(codigo) for codigo in PORTES_CATALOG]
