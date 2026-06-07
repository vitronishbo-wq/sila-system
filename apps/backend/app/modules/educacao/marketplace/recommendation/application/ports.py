"""Domain ports (interfaces) for Recommendation subdomain"""
from abc import ABC, abstractmethod
from typing import List, Optional, Any


class RecommendationModelPort(ABC):
    """Port para modelo de recomendação"""
    
    @abstractmethod
    async def get_recommendations(self, citizen_id: str, limit: int = 10) -> List[Any]:
        """Obter recomendações personalizadas"""
        pass
    
    @abstractmethod
    async def train_model(self) -> None:
        """Treinar modelo de recomendação"""
        pass


class UserPreferencesPort(ABC):
    """Port para acesso a preferências do cidadão"""
    
    @abstractmethod
    async def get_preferences(self, citizen_id: str) -> Optional[dict]:
        """Obter preferências do cidadão"""
        pass
    
    @abstractmethod
    async def save_preferences(self, citizen_id: str, preferences: dict) -> None:
        """Salvar preferências do cidadão"""
        pass
