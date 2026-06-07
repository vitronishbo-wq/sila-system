"""Application services for Matching subdomain"""
from typing import List, Optional, Any

from .ports import (
    EligibilityValidatorPort,
    CitizenProfilePort,
    MatchingEnginePort,
)


class MatchingService:
    """Serviço de aplicação para Matching"""
    
    def __init__(
        self,
        eligibility_validator: EligibilityValidatorPort,
        citizen_profile: CitizenProfilePort,
        matching_engine: MatchingEnginePort,
    ):
        self.eligibility_validator = eligibility_validator
        self.citizen_profile = citizen_profile
        self.matching_engine = matching_engine
    
    async def find_matches(self, citizen_id: str) -> List[Any]:
        """Encontrar oportunidades compatíveis"""
        # Verificar se perfil existe
        profile = await self.citizen_profile.get_profile(citizen_id)
        if not profile:
            return []
        
        # Usar matching engine
        return await self.matching_engine.find_matches(citizen_id)
    
    async def check_eligibility(self, citizen_id: str, opportunity_id: str) -> dict:
        """Verificar elegibilidade"""
        return await self.eligibility_validator.validate(citizen_id, opportunity_id)
