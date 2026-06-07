"""Application services for Search subdomain"""
from typing import List, Optional, Any

from .ports import (
    SearchEnginePort,
    GeolocationServicePort,
)


class SearchService:
    """Serviço de aplicação para Search"""
    
    def __init__(
        self,
        search_engine: SearchEnginePort,
        geolocation: GeolocationServicePort,
    ):
        self.search_engine = search_engine
        self.geolocation = geolocation
    
    async def search(self, query: str, filters: dict) -> List[Any]:
        """Buscar oportunidades"""
        return await self.search_engine.search(query, filters)
    
    async def search_nearby(
        self, 
        latitude: float, 
        longitude: float, 
        radius_km: float = 10
    ) -> List[Any]:
        """Buscar oportunidades próximas"""
        return await self.geolocation.find_nearby(latitude, longitude, radius_km)
