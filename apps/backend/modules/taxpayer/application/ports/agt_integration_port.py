from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List


class AGTIntegrationPort(ABC):
    """Interface para integração com API da AGT"""
    
    @abstractmethod
    async def validate_nif(self, nif: str) -> bool:
        """Valida se NIF existe na AGT"""
        pass
    
    @abstractmethod
    async def get_taxpayer_data(self, nif: str) -> Optional[Dict[str, Any]]:
        """Obtém dados completos do contribuinte da AGT"""
        pass
    
    @abstractmethod
    async def get_taxpayer_status(self, nif: str) -> Optional[str]:
        """Obtém status do contribuinte na AGT"""
        pass
    
    @abstractmethod
    async def get_tax_debts(self, nif: str) -> List[Dict[str, Any]]:
        """Obtém lista de dívidas do contribuinte na AGT"""
        pass
    
    @abstractmethod
    async def get_declaration_history(self, nif: str, year: Optional[int] = None) -> List[Dict[str, Any]]:
        """Obtém histórico de declarações do contribuinte"""
        pass
    
    @abstractmethod
    async def get_payment_history(self, nif: str, year: Optional[int] = None) -> List[Dict[str, Any]]:
        """Obtém histórico de pagamentos do contribuinte"""
        pass
    
    @abstractmethod
    async def submit_declaration(self, nif: str, declaration_data: Dict[str, Any]) -> str:
        """Submete uma declaração à AGT e retorna número de protocolo"""
        pass
    
    @abstractmethod
    async def check_declaration_status(self, protocol: str) -> Dict[str, Any]:
        """Verifica status de uma declaração submetida"""
        pass
    
    @abstractmethod
    async def request_certificate(self, nif: str, certificate_type: str, year: Optional[int] = None) -> str:
        """Solicita uma certidão à AGT"""
        pass
    
    @abstractmethod
    async def download_certificate(self, certificate_id: str) -> bytes:
        """Download de certidão em PDF"""
        pass
    
    @abstractmethod
    async def simulate_payment(self, nif: str, amount: float, reference: str) -> Dict[str, Any]:
        """Simula um pagamento (para testes)"""
        pass
    
    @abstractmethod
    async def confirm_payment(self, payment_data: Dict[str, Any]) -> bool:
        """Confirma um pagamento na AGT"""
        pass
    
    @abstractmethod
    async def get_tax_calendar(self, year: int) -> List[Dict[str, Any]]:
        """Obtém calendário fiscal do ano"""
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        """Verifica se API da AGT está acessível"""
        pass
