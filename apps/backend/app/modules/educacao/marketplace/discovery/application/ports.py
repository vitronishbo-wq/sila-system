"""Domain ports (interfaces) for Discovery subdomain"""
from abc import ABC, abstractmethod
from typing import List, Optional, Any


class OpportunityRepositoryPort(ABC):
    """Port para acesso a oportunidades educacionais"""
    
    @abstractmethod
    async def find_all(self, filters: Optional[dict] = None) -> List[Any]:
        """Listar todas as oportunidades com filtros opcionais"""
        pass
    
    @abstractmethod
    async def find_by_id(self, opportunity_id: str) -> Optional[Any]:
        """Encontrar oportunidade por ID"""
        pass
    
    @abstractmethod
    async def save(self, opportunity: Any) -> str:
        """Salvar nova oportunidade"""
        pass


class InstitutionRepositoryPort(ABC):
    """Port para acesso a instituições educacionais"""
    
    @abstractmethod
    async def find_all(self) -> List[Any]:
        """Listar todas as instituições"""
        pass
    
    @abstractmethod
    async def find_by_id(self, institution_id: str) -> Optional[Any]:
        """Encontrar instituição por ID"""
        pass


class ProgramRepositoryPort(ABC):
    """Port para acesso a programas educacionais"""
    
    @abstractmethod
    async def find_by_institution(self, institution_id: str) -> List[Any]:
        """Listar programas de uma instituição"""
        pass
    
    @abstractmethod
    async def find_by_id(self, program_id: str) -> Optional[Any]:
        """Encontrar programa por ID"""
        pass
