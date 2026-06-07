"""Domain ports (interfaces) for Matching subdomain"""
from abc import ABC, abstractmethod
from typing import List, Optional, Any


class EligibilityValidatorPort(ABC):
    """Port para validação de elegibilidade"""
    
    @abstractmethod
    async def validate(self, citizen_id: str, opportunity_id: str) -> dict:
        """Validar elegibilidade do cidadão para oportunidade"""
        pass
    
    @abstractmethod
    async def get_validation_rules(self, opportunity_id: str) -> dict:
        """Obter regras de validação de uma oportunidade"""
        pass


class CitizenProfilePort(ABC):
    """Port para acesso a perfil do cidadão"""
    
    @abstractmethod
    async def get_profile(self, citizen_id: str) -> Optional[Any]:
        """Obter perfil do cidadão"""
        pass
    
    @abstractmethod
    async def get_academic_history(self, citizen_id: str) -> List[Any]:
        """Obter histórico acadêmico do cidadão"""
        pass


class MatchingEnginePort(ABC):
    """Port para motor de matching"""
    
    @abstractmethod
    async def find_matches(self, citizen_id: str) -> List[Any]:
        """Encontrar oportunidades compatíveis"""
        pass
