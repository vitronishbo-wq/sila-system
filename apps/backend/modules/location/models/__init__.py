"""Location module models - Hierarchical structure and generic region support.

Exports:
- Hierarchy: CountryModel, ProvinceModel, MunicipalityModel, CommuneModel, CityModel, FullAddress
- Generic: Region
"""

from .hierarchy import (
    CountryModel,
    ProvinceModel,
    MunicipalityModel,
    CommuneModel,
    CityModel,
    FullAddressModel,
)
from .region import Region

__all__ = [
    # Hierarchical models
    "CountryModel",
    "ProvinceModel",
    "MunicipalityModel",
    "CommuneModel",
    "CityModel",
    "FullAddressModel",
    # Generic models
    "Region",
]
