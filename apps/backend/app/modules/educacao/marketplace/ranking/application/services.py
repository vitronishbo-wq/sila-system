"""Application services for Ranking subdomain"""
from typing import List, Optional, Any

from .ports import (
    InstitutionMetricsRepositoryPort,
    RankingCachePort,
)


class RankingService:
    """Serviço de aplicação para Ranking"""
    
    def __init__(
        self,
        metrics_repo: InstitutionMetricsRepositoryPort,
        cache: RankingCachePort,
    ):
        self.metrics_repo = metrics_repo
        self.cache = cache
    
    async def rank_institutions(self, sort_by: str = "quality") -> List[Any]:
        """Ranking de instituições"""
        cache_key = f"ranking:institutions:{sort_by}"
        
        # Tentar recuperar do cache
        cached_ranking = await self.cache.get_ranking(cache_key)
        if cached_ranking:
            return cached_ranking
        
        # TODO: Implementar lógica de ranking
        ranking = []
        
        # Armazenar em cache por 1 hora
        await self.cache.set_ranking(cache_key, ranking, ttl=3600)
        
        return ranking
    
    async def compare_institutions(self, institution_ids: List[str]) -> dict:
        """Comparar instituições"""
        comparison = {}
        for institution_id in institution_ids:
            metrics = await self.metrics_repo.get_metrics(institution_id)
            if metrics:
                comparison[institution_id] = metrics
        return comparison
