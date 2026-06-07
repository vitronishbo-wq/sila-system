"""Application services for Discovery subdomain"""
from typing import List, Optional, Any

from .ports import (
    OpportunityRepositoryPort,
    InstitutionRepositoryPort,
    ProgramRepositoryPort,
)


class DiscoveryService:
    """Serviço de aplicação para Discovery"""
    
    def __init__(
        self,
        opportunity_repo: OpportunityRepositoryPort,
        institution_repo: InstitutionRepositoryPort,
        program_repo: ProgramRepositoryPort,
    ):
        self.opportunity_repo = opportunity_repo
        self.institution_repo = institution_repo
        self.program_repo = program_repo
    
    async def list_opportunities(self, filters: Optional[dict] = None) -> List[Any]:
        """Listar oportunidades disponíveis"""
        return await self.opportunity_repo.find_all(filters)
    
    async def get_opportunity(self, opportunity_id: str) -> Optional[Any]:
        """Obter detalhes de uma oportunidade"""
        return await self.opportunity_repo.find_by_id(opportunity_id)
    
    async def list_institutions(self) -> List[Any]:
        """Listar instituições"""
        return await self.institution_repo.find_all()
    
    async def get_institution(self, institution_id: str) -> Optional[Any]:
        """Obter detalhes de uma instituição"""
        return await self.institution_repo.find_by_id(institution_id)
    
    async def list_programs(self, institution_id: Optional[str] = None) -> List[Any]:
        """Listar programas"""
        if institution_id:
            return await self.program_repo.find_by_institution(institution_id)
        return []
