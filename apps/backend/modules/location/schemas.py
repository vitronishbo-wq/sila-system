"""
Location Schemas Module
Refatorado para suportar a estrutura unificada de locations e árvores recursivas.
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict


# --- Schemas Básicos de Região ---

class RegionBase(BaseModel):
    name: str
    type: str  # "PAIS" | "PROVINCIA" | "MUNICIPIO" | "COMUNA"


class RegionCreate(RegionBase):
    parent_id: Optional[int] = None


class RegionUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    parent_id: Optional[int] = None


class RegionResponse(RegionBase):
    id: int
    parent_id: Optional[int] = None
    
    model_config = ConfigDict(from_attributes=True)


# --- Schemas de Árvore (Recursivos) ---

class RegionTree(RegionResponse):
    """
    Schema recursivo para retornar a hierarquia completa da DPA.
    Ex: Província -> Municípios -> Comunas.
    """
    children: List["RegionTree"] = []

    model_config = ConfigDict(from_attributes=True)


# --- Endereços e Localização Completa ---

class FullAddressResponse(BaseModel):
    id: int
    street: Optional[str] = None
    number: Optional[str] = None
    zip_code: Optional[str] = None
    region_id: int  # Aponta para a tabela unificada locations

    model_config = ConfigDict(from_attributes=True)


class LocationHierarchy(BaseModel):
    """Utilizado para carregar a trilha de navegação (Breadcrumbs)."""
    id: int
    name: str
    type: str
    parent: Optional["LocationHierarchy"] = None

    model_config = ConfigDict(from_attributes=True)


# --- Países ---

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
    model_config = ConfigDict(from_attributes=True)


# --- Aliases para Compatibilidade (Fix para ImportError no __init__) ---

# Províncias
ProvinceCreate = RegionCreate
ProvinceUpdate = RegionUpdate
ProvinceResponse = RegionResponse

# Municípios
MunicipalityCreate = RegionCreate
MunicipalityUpdate = RegionUpdate
MunicipalityResponse = RegionResponse

# Comunas
CommuneCreate = RegionCreate
CommuneUpdate = RegionUpdate
CommuneResponse = RegionResponse

# Árvores (Tree aliases)
ProvinceTree = RegionTree
MunicipalityTree = RegionTree
CommuneTree = RegionTree

# Necessário para referências circulares no Pydantic
RegionTree.model_rebuild()
LocationHierarchy.model_rebuild()