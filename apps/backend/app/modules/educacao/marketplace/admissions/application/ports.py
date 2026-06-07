"""Domain ports (interfaces) for Admissions subdomain"""
from abc import ABC, abstractmethod
from typing import Optional, Any, List


class AdmissionRepositoryPort(ABC):
    """Port para acesso a admissões"""
    
    @abstractmethod
    async def create_admission(self, citizen_id: str, opportunity_id: str) -> str:
        """Criar processo de admissão"""
        pass
    
    @abstractmethod
    async def get_admission(self, admission_id: str) -> Optional[Any]:
        """Obter detalhes da admissão"""
        pass
    
    @abstractmethod
    async def update_admission_status(self, admission_id: str, status: str) -> None:
        """Atualizar status da admissão"""
        pass


class EligibilityValidatorPort(ABC):
    """Port para validação de elegibilidade"""
    
    @abstractmethod
    async def validate_eligibility(self, citizen_id: str, opportunity_id: str) -> dict:
        """Validar elegibilidade para admissão"""
        pass


class DocumentVerificationPort(ABC):
    """Port para verificação de documentos"""
    
    @abstractmethod
    async def verify_documents(self, citizen_id: str, required_docs: List[str]) -> dict:
        """Verificar documentos obrigatórios"""
        pass
    
    @abstractmethod
    async def get_missing_documents(self, citizen_id: str, required_docs: List[str]) -> List[str]:
        """Obter documentos faltando"""
        pass
