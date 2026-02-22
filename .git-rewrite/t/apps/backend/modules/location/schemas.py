"""
Location Schemas Module

Schemas para entidades de localização no SILA system.
Inclui Países, Províncias, Municípios, Regiões, Comunas e Cidades,
bem como respostas de endereço e hierarquia de localização.
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict


# ---------------------------
# Country Schemas
# ---------------------------


class CountryBase(BaseModel):
    name: str
    code: str


class CountryCreate(CountryBase):
    pass


class CountryUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None


class CountryResponse(CountryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ---------------------------
# Province Schemas
# ---------------------------


class ProvinceBase(BaseModel):
    name: str
    country_id: int


class ProvinceCreate(ProvinceBase):
    pass


class ProvinceUpdate(BaseModel):
    name: Optional[str] = None
    country_id: Optional[int] = None


class ProvinceResponse(ProvinceBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ---------------------------
# Municipality Schemas
# ---------------------------


class MunicipalityBase(BaseModel):
    name: str
    province_id: int


class MunicipalityCreate(MunicipalityBase):
    pass


class MunicipalityUpdate(BaseModel):
    name: Optional[str] = None
    province_id: Optional[int] = None


class MunicipalityResponse(MunicipalityBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ---------------------------
# Region Schemas
# ---------------------------


class RegionBase(BaseModel):
    name: str
    type: str  # "municipio" | "provincia" | "pais"


class RegionCreate(RegionBase):
    parent_id: Optional[int] = None


class RegionUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    parent_id: Optional[int] = None


class Region(RegionBase):
    id: int
    parent_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ---------------------------
# Commune Schemas
# ---------------------------


class CommuneBase(BaseModel):
    name: str
    city_id: int


class CommuneCreate(CommuneBase):
    pass


class CommuneUpdate(BaseModel):
    name: Optional[str] = None
    city_id: Optional[int] = None


class Commune(CommuneBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ---------------------------
# City Schemas
# ---------------------------


class CityBase(BaseModel):
    name: str
    region_id: int


class CityCreate(CityBase):
    pass


class CityUpdate(BaseModel):
    name: Optional[str] = None
    region_id: Optional[int] = None


class City(CityBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CityResponse(BaseModel):
    id: int
    name: str
    commune_id: int

    model_config = ConfigDict(from_attributes=True)


# ---------------------------
# Address & Hierarchy Schemas
# ---------------------------


class FullAddressResponse(BaseModel):
    id: int
    street: Optional[str] = None
    number: Optional[str] = None
    zip_code: Optional[str] = None
    commune_id: int

    model_config = ConfigDict(from_attributes=True)


class LocationHierarchy(BaseModel):
    country: CountryResponse
    provinces: List[ProvinceResponse]
    municipalities: List[MunicipalityResponse]
    communes: List[Commune]

    model_config = ConfigDict(from_attributes=True)
