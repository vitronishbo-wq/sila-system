from __future__ import annotations
from apps.backend.app.modules.economy.trade.services.domain.enums import PorteComercial, RamoComercial
from apps.backend.app.modules.economy.trade.services.domain.models.porte_comercial import PorteComercio
from apps.backend.app.modules.economy.trade.services.domain.models.ramo_comercial import RamoComercio
RAMOS_CATALOG: dict[RamoComercial, str] = {RamoComercial.VAREJISTA: 'Comercio varejista', RamoComercial.ATACADISTA: 'Comercio atacadista', RamoComercial.ELETRONICO: 'Comercio eletronico', RamoComercial.SUPERMERCADO: 'Supermercado', RamoComercial.FARMACIA: 'Farmacia e drogaria', RamoComercial.VESTUARIO: 'Vestuario', RamoComercial.CALCADOS: 'Calcados', RamoComercial.MOVEIS: 'Moveis e decoracao', RamoComercial.ELETRODOMESTICOS: 'Eletrodomesticos', RamoComercial.ELETRONICOS: 'Eletronicos e informatica', RamoComercial.MATERIAL_CONSTRUCAO: 'Material de construcao', RamoComercial.AUTOMOTIVO: 'Comercio automotivo', RamoComercial.ALIMENTACAO: 'Alimentacao', RamoComercial.BEBIDAS: 'Bebidas', RamoComercial.COMBUSTIVEL: 'Combustivel', RamoComercial.SERVICOS: 'Prestacao de servicos', RamoComercial.SAUDE: 'Saude comercial', RamoComercial.EDUCACAO: 'Educacao comercial', RamoComercial.HOSPEDAGEM: 'Hospedagem', RamoComercial.LAZER: 'Lazer e entretenimento', RamoComercial.CULTURA: 'Cultura', RamoComercial.FINANCEIRO: 'Servicos financeiros', RamoComercial.IMOBILIARIO: 'Servicos imobiliarios'}
PORTES_CATALOG: dict[PorteComercial, str] = {PorteComercial.MICRO: 'Micro empreendimento comercial', PorteComercial.PEQUENA: 'Pequeno empreendimento comercial', PorteComercial.MEDIA: 'Medio empreendimento comercial', PorteComercial.GRANDE: 'Grande empreendimento comercial', PorteComercial.EMPORIO: 'Emporio comercial'}

def get_ramo(codigo: RamoComercial) -> RamoComercio:
    return RamoComercio(codigo=codigo, descricao=RAMOS_CATALOG[codigo])

def get_porte(codigo: PorteComercial) -> PorteComercio:
    return PorteComercio(codigo=codigo, descricao=PORTES_CATALOG[codigo])

def list_ramos() -> list[RamoComercio]:
    return [get_ramo(codigo) for codigo in RAMOS_CATALOG]

def list_portes() -> list[PorteComercio]:
    return [get_porte(codigo) for codigo in PORTES_CATALOG]