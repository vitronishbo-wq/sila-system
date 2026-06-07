"""Domain ports (interfaces) for Ranking subdomain"""
from abc import ABC, abstractmethod
from typing import List, Optional, Any


class InstitutionMetricsRepositoryPort(ABC):
    """Port para acesso a métricas de instituições"""
    
    @abstractmethod
    async def get_metrics(self, institution_id: str) -> Optional[Any]:
        """Obter métricas de uma instituição"""
        pass
    
    @abstractmethod
    async def update_metrics(self, institution_id: str, metrics: dict) -> None:
        """Atualizar métricas de instituição"""
        pass


class RankingCachePort(ABC):
    """Port para cache de rankings"""
    
    @abstractmethod
    async def get_ranking(self, key: str) -> Optional[List[Any]]:
        """Obter ranking do cache"""
        pass
    
    @abstractmethod
    async def set_ranking(self, key: str, ranking: List[Any], ttl: int) -> None:
        """Armazenar ranking em cache"""
        pass
