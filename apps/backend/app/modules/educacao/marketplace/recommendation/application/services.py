"""Application services for Recommendation subdomain"""
from typing import List, Optional, Any

from .ports import (
    RecommendationModelPort,
    UserPreferencesPort,
)


class RecommendationService:
    """Serviço de aplicação para Recommendation"""
    
    def __init__(
        self,
        model: RecommendationModelPort,
        preferences: UserPreferencesPort,
    ):
        self.model = model
        self.preferences = preferences
    
    async def get_recommendations(self, citizen_id: str, limit: int = 10) -> List[Any]:
        """Obter recomendações personalizadas"""
        # Verificar preferências
        prefs = await self.preferences.get_preferences(citizen_id)
        
        # Obter recomendações do modelo
        return await self.model.get_recommendations(citizen_id, limit)
    
    async def update_preferences(self, citizen_id: str, preferences: dict) -> None:
        """Atualizar preferências do cidadão"""
        await self.preferences.save_preferences(citizen_id, preferences)
