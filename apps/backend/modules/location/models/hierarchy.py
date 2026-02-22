# modules/location/models/hierarchy.py
"""
Hierarchical location models - Tabela Única (locations)

Utiliza a model Region como base para toda a hierarquia:
 - Country
 - Province
 - Municipality
 - Commune

Aliases mantidos para compatibilidade com código antigo.
"""

from modules.location.models.region import Region

# Aliases para evitar breaking changes em imports antigos
CountryModel = Region
ProvinceModel = Region
MunicipalityModel = Region
CommuneModel = Region
CityModel = Region
FullAddressModel = Region

__all__ = [
    "Region",
    "CountryModel",
    "ProvinceModel",
    "MunicipalityModel",
    "CommuneModel",
    "CityModel",
    "FullAddressModel",
]
