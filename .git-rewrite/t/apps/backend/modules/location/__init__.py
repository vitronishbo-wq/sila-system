"""
Core Location Module

This module handles the hierarchical location structure:
Country → Province → Municipality → Commune

Provides services for location management and address validation.
"""

"""Module initialization with path configuration."""

import sys
from pathlib import Path

# Ensure backend is in path for imports
_backend_path = Path(__file__).parent.parent.parent
if str(_backend_path) not in sys.path:
    sys.path.insert(0, str(_backend_path))

from .schemas import (
    CommuneCreate,
    CommuneUpdate,
    Commune,
    RegionCreate,
    RegionUpdate,
    Region,
    CityCreate,
    CityUpdate,
    City,
    CountryCreate,
    CountryUpdate,
    CountryResponse,
    FullAddressResponse,
    LocationHierarchy,
    MunicipalityCreate,
    MunicipalityUpdate,
    MunicipalityResponse,
    ProvinceCreate,
    ProvinceUpdate,
    ProvinceResponse,
)
from .services import LocationService

__all__ = [
    "LocationService",
    "CountryCreate",
    "CountryUpdate",
    "CountryResponse",
    "ProvinceCreate",
    "ProvinceUpdate",
    "ProvinceResponse",
    "MunicipalityCreate",
    "MunicipalityUpdate",
    "MunicipalityResponse",
    "CommuneCreate",
    "CommuneUpdate",
    "Commune",
    "RegionCreate",
    "RegionUpdate",
    "Region",
    "CityCreate",
    "CityUpdate",
    "City",
    "FullAddressResponse",
    "LocationHierarchy",
]
