# modules/location/models/location.py
"""
Ponto de entrada para os modelos de localização.
Redireciona as definições do hierarchy para manter compatibilidade.
"""

from .hierarchy import (
    CountryModel,
    ProvinceModel,
    MunicipalityModel,
    CommuneModel,
    CityModel,
    FullAddressModel
)

# Exporta explicitamente para facilitar o acesso externo
__all__ = [
    "CountryModel",
    "ProvinceModel",
    "MunicipalityModel",
    "CommuneModel",
    "CityModel",
    "FullAddressModel"
]