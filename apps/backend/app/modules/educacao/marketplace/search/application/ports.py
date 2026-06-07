"""Domain ports (interfaces) for Search subdomain"""
from abc import ABC, abstractmethod
from typing import List, Optional, Any


class SearchEnginePort(ABC):
    """Port para motor de busca"""
    
    @abstractmethod
    async def search(self, query: str, filters: dict) -> List[Any]:
        """Buscar oportunidades com filtros"""
        pass
    
    @abstractmethod
    async def index_document(self, doc_id: str, document: dict) -> None:
        """Indexar documento para busca"""
        pass


class GeolocationServicePort(ABC):
    """Port para serviço de geolocalização"""
    
    @abstractmethod
    async def find_nearby(self, latitude: float, longitude: float, radius_km: float) -> List[Any]:
        """Encontrar oportunidades próximas"""
        pass
    
    @abstractmethod
    async def calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calcular distância entre dois pontos"""
        pass
