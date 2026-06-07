"""Domain ports (interfaces) for Transfers subdomain"""
from abc import ABC, abstractmethod
from typing import Optional, Any, List


class TransferRepositoryPort(ABC):
    """Port para acesso a transferências"""
    
    @abstractmethod
    async def create_transfer_request(self, transfer_data: dict) -> str:
        """Criar solicitação de transferência"""
        pass
    
    @abstractmethod
    async def get_transfer(self, transfer_id: str) -> Optional[Any]:
        """Obter detalhes da transferência"""
        pass


class CurriculumValidatorPort(ABC):
    """Port para validação de currículo"""
    
    @abstractmethod
    async def check_compatibility(self, source_program_id: str, destination_program_id: str) -> dict:
        """Verificar compatibilidade curricular"""
        pass
    
    @abstractmethod
    async def get_credit_mapping(self, source_program_id: str, destination_program_id: str) -> List[dict]:
        """Obter mapeamento de créditos"""
        pass


class TransferValidatorPort(ABC):
    """Port para validação de transferência"""
    
    @abstractmethod
    async def validate_transfer_request(self, citizen_id: str, source_id: str, destination_id: str) -> dict:
        """Validar solicitação de transferência"""
        pass
